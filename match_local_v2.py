# -*- coding: utf-8 -*-
"""
match_local.py (정확도 강화판)
─────────────────────────────────────────────────────────────
download_tour.py 가 받아둔 tour_places.json 을 읽어서
성지(pilgrimages)와 로컬에서 좌표+이름 매칭 → 사진·주소·전화 저장.
API 호출 없음(로컬 계산만) → 빠르고 한도 걱정 없음.

[기존 버전과 다른 점]
기존엔 반경 안에서 "제일 가까운 곳"을 무조건 매칭했음(이름 확인 없음).
→ 좁은 골목에 여러 시설이 붙어있으면 엉뚱한 곳이 매칭될 위험이 있었음.
이번 버전은 반경 조건 + "이름이 실제로 비슷한지"까지 같이 확인해서,
둘 다 통과해야 매칭시킴. 애매하면 매칭 안 시키는 쪽을 선택함
(잘못된 사진이 붙는 것보다, 안 붙는 게 낫다는 원칙 — map.html의
matchTourContentIdStrict()와 같은 철학).

반경(RADIUS)·이름유사도(NAME_THRESHOLD)를 바꿔가며 몇 번이고 다시 돌려도 됨.
"""

import json
import math
import re
import firebase_admin
from firebase_admin import credentials, firestore

# ═════════════════════════════════════════════════════════════
FIREBASE_KEY = r"D:\python\starspoon-120d7-firebase-adminsdk-fbsvc-e4875887a9.json"
# 직장 PC면: r"C:\Users\Admin\Desktop\파이션\starspoon-120d7-firebase-adminsdk-fbsvc-c88385de0a.json"
RADIUS = 500          # 매칭 반경(m). 넓히면 후보↑ (좀 먼 것도 후보에 포함)
NAME_THRESHOLD = 0.5  # 이름 유사도 최소 기준(0~1). 낮추면 매칭↑(부정확 위험도↑)
# ═════════════════════════════════════════════════════════════

TOUR_FILE = "tour_places.json"

cred = credentials.Certificate(FIREBASE_KEY)
firebase_admin.initialize_app(cred)
db = firestore.client()


def haversine(lat1, lng1, lat2, lng2):
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def normalize_for_match(s: str) -> str:
    s = s or ""
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[\s\-_·,\.]", "", s)
    return s.lower()


def bigrams(s: str):
    return {s[i:i + 2] for i in range(len(s) - 1)}


def name_similarity(a: str, b: str) -> float:
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


def main():
    with open(TOUR_FILE, "r", encoding="utf-8") as f:
        tours = json.load(f)
    print(f"관광지 목록: {len(tours)}곳 로드")

    # 격자 인덱스 (0.05도 ≈ 5km 셀) — 빠른 근처 검색용
    grid = {}
    for t in tours:
        key = (round(t["lat"] / 0.05), round(t["lng"] / 0.05))
        grid.setdefault(key, []).append(t)

    def nearby(lat, lng):
        gy, gx = round(lat / 0.05), round(lng / 0.05)
        out = []
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                out.extend(grid.get((gy + dy, gx + dx), []))
        return out

    print("성지 로딩 중...")
    docs = list(db.collection("pilgrimages").stream())
    print(f"성지 {len(docs)}개\n")

    matched, no_candidate, rejected_by_name = 0, 0, 0
    batch = db.batch()
    batch_cnt = 0

    for doc in docs:
        d = doc.to_dict()
        lat, lng = d.get("lat"), d.get("lng")
        place_name = d.get("placeName", "")
        if not lat or not lng:
            continue

        cands = nearby(lat, lng)
        # 반경 안의 후보들 중, "이름 유사도"가 가장 높은 것을 고른다
        # (기존처럼 무조건 최단거리를 고르지 않음 — 가까워도 이름이 다르면 탈락)
        best, best_dist, best_name_score = None, 1e9, 0.0
        for t in cands:
            dist = haversine(lat, lng, t["lat"], t["lng"])
            if dist > RADIUS:
                continue
            score = name_similarity(place_name, t.get("title", ""))
            if score > best_name_score or (score == best_name_score and dist < best_dist):
                best, best_dist, best_name_score = t, dist, score

        if best is None:
            update = {"tourChecked": True, "tourMatched": False}
            no_candidate += 1
        elif best_name_score < NAME_THRESHOLD:
            update = {"tourChecked": True, "tourMatched": False}
            rejected_by_name += 1
        else:
            update = {
                "tourChecked": True, "tourMatched": True,
                "tourContentId": best["contentid"],
                "tourTitle": best["title"],
                "tourImage": best["firstimage"],
                "tourAddr": best["addr1"],
                "tourTel": best["tel"],
                "tourDist": round(best_dist),
                "tourNameScore": round(best_name_score, 2),
            }
            matched += 1

        batch.update(doc.reference, update)
        batch_cnt += 1

        if batch_cnt >= 450:
            batch.commit()
            batch = db.batch()
            batch_cnt = 0
            print(f"   ...진행 (매칭 {matched} · 이름불일치로 제외 {rejected_by_name} · 후보없음 {no_candidate})")

    if batch_cnt > 0:
        batch.commit()

    print("\n" + "=" * 50)
    print(f"매칭 완료: 매칭 {matched}곳")
    print(f"반경 안에는 있었지만 이름이 안 비슷해서 제외: {rejected_by_name}곳")
    print(f"반경 안에 후보 자체가 없음: {no_candidate}곳")
    print(f"반경 {RADIUS}m / 이름유사도 {NAME_THRESHOLD} 기준.")
    print("매칭을 더 늘리려면 RADIUS를 넓히거나 NAME_THRESHOLD를 낮추고 다시 실행하세요.")
    print("(이미 매칭된 문서도 이번 실행에서 덮어쓰니, 기준 바꿔서 재실행해도 안전합니다)")


if __name__ == "__main__":
    main()
