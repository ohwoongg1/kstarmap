# -*- coding: utf-8 -*-
"""
match_tour_content_id.py
─────────────────────────────────────────────────────────
Firestore의 pilgrimages 컬렉션(9,574곳)을 관광공사 TourAPI와
좌표 기반으로 매칭해서 tourContentId 필드를 채워넣는 스크립트.

tourContentId가 채워지면 map.html의 fetchLiveTourPhotos()가
그 순간 실시간으로 사진을 불러올 수 있게 됨 ("📡 한국관광공사 실시간 사진").

[사전 준비]
1. pip install firebase-admin requests --break-system-packages
   (사내 파이썬 환경이면 --break-system-packages 없이)

2. Firebase 콘솔 → 프로젝트 설정(톱니바퀴) → 서비스 계정
   → "새 비공개 키 생성" → 다운로드된 JSON 파일을
   이 스크립트와 같은 폴더에 두고 아래 SERVICE_ACCOUNT_PATH에
   파일명을 정확히 맞춰줄 것 (절대 git에 커밋하지 말 것!)

3. python match_tour_content_id.py
   → 실행하면 자동으로 이어서(resume) 처리함.
     이미 tourContentId가 있는 문서는 건너뜀.
     하루 트래픽 한도(개발계정 1,000건)에 걸리면 자동으로 멈추고
     다음날 다시 실행하면 안 한 것부터 이어서 진행됨.

[결과물]
- Firestore pilgrimages 문서에 tourContentId 필드 추가
- tour_match_log.csv 파일에 처리 내역 전부 기록
  (장소명, 매칭된 관광공사 제목, 유사도 점수, 상태)
  → 유사도가 낮은(예: 0.5~0.7) 매칭은 사람이 한 번 훑어보고
    확인하는 걸 권장함. 엉뚱한 곳이 매칭될 수 있음.
"""

import csv
import os
import re
import sys
import time

import requests
import firebase_admin
from firebase_admin import credentials, firestore

# ── 설정 ──────────────────────────────────────────────
SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"   # 다운로드한 파일명으로 수정
TOUR_API_KEY = "1841b269a603176ed99db0c0ab7f40a30a71ab76aed77c4e1da671ffa3468e2"

# map.html의 PhotoGalleryService1과 같은 버전(B551011/KorService1)으로 통일
LOCATION_BASED_URL = "https://apis.data.go.kr/B551011/KorService1/locationBasedList1"

RADIUS_METERS = 300        # 좌표 반경 300m 안에서 검색
# map.html의 matchTourContentIdStrict()와 동일한 엄격 기준.
# 잘못된 콘텐츠가 매칭되는 것보다, 매칭 안 되는 게 낫다는 원칙 — 아주 확실할 때만 채움.
MATCH_THRESHOLD = 0.92
SLEEP_SECONDS = 0.35       # 호출 간 간격(과도한 트래픽 방지)
LOG_PATH = "tour_match_log.csv"
COLLECTION = "pilgrimages"


def normalize_for_match(s: str) -> str:
    """공백/괄호/구두점 제거 + 소문자화. map.html normalizeForMatch()와 동일."""
    s = s or ""
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[\s\-_·,\.]", "", s)
    return s.lower()


def bigrams(s: str):
    return {s[i:i + 2] for i in range(len(s) - 1)}


def name_similarity(a: str, b: str) -> float:
    """map.html nameSimilarity()와 동일한 로직(Dice 2-gram 유사도 + 포함관계 보정)."""
    a, b = normalize_for_match(a), normalize_for_match(b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if len(a) >= 3 and len(b) >= 3 and (a in b or b in a):
        return 0.95
    ga, gb = bigrams(a), bigrams(b)
    if not ga or not gb:
        return 0.0
    inter = len(ga & gb)
    return (2 * inter) / (len(ga) + len(gb))


def find_content_id(lat: float, lng: float, place_name: str):
    """좌표 반경 내 관광공사 콘텐츠 중 이름이 가장 비슷한 것을 찾아 반환.
    반환값: (contentId 또는 None, 매칭된 제목, 유사도 점수, 원본 응답 상태)
    """
    params = {
        "serviceKey": TOUR_API_KEY,
        "numOfRows": 10,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "KStarMap",
        "_type": "json",
        "mapX": lng,
        "mapY": lat,
        "radius": RADIUS_METERS,
        "arrange": "E",  # 거리순 정렬
    }
    try:
        res = requests.get(LOCATION_BASED_URL, params=params, timeout=10)
    except requests.RequestException as e:
        return None, None, 0.0, f"요청 실패: {e}"

    if res.status_code != 200:
        return None, None, 0.0, f"HTTP {res.status_code}"

    try:
        data = res.json()
    except ValueError:
        # 트래픽 초과 시 XML 에러가 돌아오는 경우가 있음
        text = res.text[:200]
        if "LIMITED_NUMBER_OF_SERVICE_REQUESTS" in text or "SERVICE_KEY" in text:
            return None, None, 0.0, "QUOTA_EXCEEDED"
        return None, None, 0.0, f"JSON 파싱 실패: {text}"

    header = data.get("response", {}).get("header", {})
    result_code = header.get("resultCode")
    if result_code not in (None, "0000", "00"):
        result_msg = header.get("resultMsg", "")
        if "LIMITED" in result_msg or "trafficCount" in result_msg.lower():
            return None, None, 0.0, "QUOTA_EXCEEDED"
        return None, None, 0.0, f"API 오류: {result_msg}"

    items = data.get("response", {}).get("body", {}).get("items")
    if not items:
        return None, None, 0.0, "결과없음"
    items = items.get("item") if isinstance(items, dict) else None
    if not items:
        return None, None, 0.0, "결과없음"
    if isinstance(items, dict):
        items = [items]

    best_item, best_score = None, 0.0
    for it in items:
        title = it.get("title", "")
        score = name_similarity(place_name, title)
        if score > best_score:
            best_score, best_item = score, it

    if best_item and best_score >= MATCH_THRESHOLD:
        return best_item.get("contentid"), best_item.get("title"), best_score, "매칭성공"
    matched_title = best_item.get("title") if best_item else ""
    return None, matched_title, best_score, "유사도부족"


def main():
    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        print(f"[오류] 서비스 계정 키 파일을 찾을 수 없습니다: {SERVICE_ACCOUNT_PATH}")
        print("Firebase 콘솔 → 프로젝트 설정 → 서비스 계정 → 새 비공개 키 생성 후")
        print("이 스크립트와 같은 폴더에 두고 파일명을 맞춰주세요.")
        sys.exit(1)

    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    log_exists = os.path.exists(LOG_PATH)
    log_file = open(LOG_PATH, "a", newline="", encoding="utf-8-sig")
    writer = csv.writer(log_file)
    if not log_exists:
        writer.writerow(["문서ID", "장소명", "매칭제목", "contentId", "유사도", "상태"])

    docs = list(db.collection(COLLECTION).stream())
    total = len(docs)
    print(f"pilgrimages 총 {total}건 로드 완료. 매칭 시작...\n")

    matched, already, failed, quota_stop = 0, 0, 0, False

    for i, doc in enumerate(docs, 1):
        data = doc.to_dict()

        if data.get("tourContentId"):
            already += 1
            continue

        place_name = data.get("placeName", "")
        lat, lng = data.get("lat"), data.get("lng")

        if not lat or not lng:
            writer.writerow([doc.id, place_name, "", "", "", "좌표없음"])
            continue

        content_id, matched_title, score, status = find_content_id(lat, lng, place_name)

        if status == "QUOTA_EXCEEDED":
            print(f"\n[{i}/{total}] 일일 트래픽 한도 초과로 중단합니다. 내일 다시 실행하면 이어서 진행됩니다.")
            quota_stop = True
            break

        if content_id:
            doc.reference.update({"tourContentId": content_id})
            matched += 1
            print(f"[{i}/{total}] ✅ {place_name} → {matched_title} (contentId {content_id}, 유사도 {score:.2f})")
        else:
            failed += 1
            print(f"[{i}/{total}] ❌ {place_name} — {status} (가장 근접: {matched_title or '없음'}, 유사도 {score:.2f})")

        writer.writerow([doc.id, place_name, matched_title or "", content_id or "", f"{score:.2f}", status])
        log_file.flush()
        time.sleep(SLEEP_SECONDS)

    log_file.close()

    print("\n──────────────────────────────")
    print(f"이미 매칭됨(건너뜀): {already}건")
    print(f"이번에 새로 매칭: {matched}건")
    print(f"매칭 실패: {failed}건")
    if quota_stop:
        print("⚠ 트래픽 한도로 중단됨 — 내일 다시 실행하면 자동으로 이어서 진행됩니다.")
    print(f"상세 로그: {LOG_PATH}")


if __name__ == "__main__":
    main()
