# -*- coding: utf-8 -*-
r"""
gen_share_pages.py
─────────────────────────────────────────────────────────────
한류정보창고 게시글마다 og:title/og:description/og:image가 그 글에 맞게
뜨는 정적 공유용 페이지(/post/{글ID}/index.html)를 생성한다.

카카오톡·페이스북 같은 SNS 봇은 자바스크립트를 실행하지 않기 때문에,
map.html(SPA) 자체는 어떤 글이든 항상 똑같은 기본 OG 태그만 보여준다.
그래서 글마다 "정적" HTML 한 장을 미리 만들어두고, sharePost()가
그 정적 페이지 링크를 공유하도록 바꾼다. 사람이 그 링크를 클릭하면
1초 안에 자동으로 실제 지도 앱(map.html?post=글ID)으로 넘어간다.

[사전 준비]
1. pip install firebase-admin --break-system-packages
2. D:\python\ 안의 서비스 계정 키(starspoon-120d7-firebase-adminsdk-...json)를
   이 스크립트와 같은 폴더에 두거나, 아래 SERVICE_ACCOUNT_PATH를 그 경로로 수정

[실행]
python gen_share_pages.py
→ 이 스크립트와 같은 폴더에 post/ 디렉터리가 생성됨
→ 그 post/ 폴더를 통째로 C:\Users\82102\Desktop\kstarmap\ 안에 복사
→ 평소처럼 git add / commit / push

[운영]
글을 새로 쓰거나 수정할 때마다 이 스크립트를 다시 돌려서 push하면 됨.
매번 전체를 다시 만들기 때문에(덮어쓰기), 몇 번을 돌려도 안전함.
"""

import os
import re
import json
import firebase_admin
from firebase_admin import credentials, firestore

# ═════════════════════════════════════════════════════════════
SERVICE_ACCOUNT_PATH = r"D:\python\starspoon-120d7-firebase-adminsdk-fbsvc-e4875887a9.json"
SITE_URL = "https://kstarmap.com"
DEFAULT_IMAGE = "https://kstarmap.com/og-default.jpg"  # 대표사진 없을 때 쓸 기본 배너(직접 준비해서 업로드 필요)
OUT_DIR = "post"
# ═════════════════════════════════════════════════════════════

cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()


def strip_tags_and_shorten(body: str, limit: int = 90) -> str:
    """본문에서 [성지:...], [드라마] 같은 태그, 유튜브 링크, 특수기호 라인을 제거하고
    사람이 읽을 만한 첫 문단만 뽑아 설명글로 축약."""
    text = body or ""
    text = re.sub(r"\[성지:[^\]]+\]", "", text)
    text = re.sub(r"\[[가-힣]{1,4}\]", "", text)  # [드라마][영화][음악][맛집][쇼핑][인물] 등
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[━─═\-]{3,}", "", text)
    text = re.sub(r"🔹|💬|📍|📡|kstarmap 작성", "", text)
    text = re.sub(r"#\S+", "", text)  # 해시태그
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[:limit].rstrip() + "…"
    return text


def find_thumbnail(body: str) -> str:
    """본문의 첫 [성지:장소명:...] 태그로 pilgrimages에서 대표사진을 찾아본다."""
    m = re.search(r"\[성지:([^:\]]+)", body or "")
    if not m:
        return DEFAULT_IMAGE
    place_name = m.group(1).strip()
    try:
        docs = list(
            db.collection("pilgrimages")
            .where("placeName", "==", place_name)
            .limit(1)
            .stream()
        )
        if docs:
            d = docs[0].to_dict()
            img = d.get("tourImage") or (d.get("tourImages") or [None])[0]
            if img:
                return img
    except Exception as e:
        print("  썸네일 조회 실패:", e)
    return DEFAULT_IMAGE


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta property="og:type" content="article">
<meta property="og:site_name" content="KStarMap">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{image}">
<meta http-equiv="refresh" content="0; url={redirect}">
<link rel="canonical" href="{redirect}">
<script>location.replace("{redirect}");</script>
</head>
<body>
<p>잠시 후 이동합니다… <a href="{redirect}">여기를 눌러주세요</a></p>
</body>
</html>
"""


def main():
    posts = list(db.collection("board").stream())
    print(f"게시글 {len(posts)}개 로드 완료. 공유 페이지 생성 중...")

    os.makedirs(OUT_DIR, exist_ok=True)
    made = 0

    for doc in posts:
        pid = doc.id
        data = doc.to_dict()
        title = data.get("title") or "KStarMap 한류 이야기"
        body = data.get("body") or ""
        desc = strip_tags_and_shorten(body) or "좋아하는 드라마·아티스트의 실제 성지를 지도에서 만나보세요."
        image = find_thumbnail(body)
        redirect = f"{SITE_URL}/map.html?post={pid}"
        url = f"{SITE_URL}/post/{pid}/"

        page_dir = os.path.join(OUT_DIR, pid)
        os.makedirs(page_dir, exist_ok=True)
        html = PAGE_TEMPLATE.format(
            title=esc(title),
            desc=esc(desc),
            image=esc(image),
            url=esc(url),
            redirect=esc(redirect),
        )
        with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        made += 1
        if made % 50 == 0:
            print(f"  ...{made}/{len(posts)}개 생성")

    print("\n" + "=" * 50)
    print(f"완료: {made}개 공유 페이지 생성됨 ({OUT_DIR}/ 폴더)")
    print(f"이 폴더를 kstarmap 프로젝트 루트로 복사한 뒤 git add/commit/push 하세요.")


if __name__ == "__main__":
    main()
