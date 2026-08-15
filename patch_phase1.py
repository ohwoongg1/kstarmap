#!/usr/bin/env python3
"""KStarMap Phase 1 보충 패치 — 로고/검색바/네비 HTML + CSS"""
import sys, os

path = r"C:\Users\82102\Desktop\kstarmap\map.html"
if not os.path.exists(path):
    print(f"[ERR] 파일 없음: {path}")
    sys.exit(1)

with open(path, "r", encoding="utf-8") as f:
    txt = f.read()

patches = []

# ── 1. 로고 HTML ──
patches.append((
    '<div class="logo">⭐ KStar</div>',
    '''<div class="logo">
      <svg class="logo-icon" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="16" r="15" fill="oklch(0.62 0.155 65)"/>
        <path d="M16 7l2.47 5.76L24.5 13.5l-4.5 4 1.27 6L16 20.5l-5.27 3 1.27-6-4.5-4 6.03-.74Z" fill="#fff"/>
      </svg>
      <div class="logo-text">K<span>Star</span>Map</div>
    </div>''',
    "로고 SVG"
))

# ── 2. 검색 아이콘 ──
patches.append((
    '<span style="font-size:15px;color:var(--text3)">🔍</span>',
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35"/></svg>',
    "검색 아이콘 SVG"
))

# ── 3. 햄버거 버튼 ──
patches.append((
    'style="flex-shrink:0;background:#c0392b;border:1px solid #a93226;border-radius:8px;padding:6px 7px;font-size:14px;font-weight:700;color:#fff;cursor:pointer">☰</button>',
    'style="flex-shrink:0;background:var(--gold);border:none;border-radius:10px;padding:7px 8px;cursor:pointer;display:flex;align-items:center;justify-content:center" aria-label="메뉴"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>',
    "햄버거 버튼"
))

# ── 4. 하단 네비 아이콘 (5개) ──
nav_pairs = [
    ('🗺️</div><div class="tx">지도',
     '<svg viewBox="0 0 24 24"><path d="M9 2L3 5v17l6-3 6 3 6-3V2l-6 3-6-3z"/><path d="M9 2v17M15 5v17"/></svg></div><div class="tx">지도',
     "네비-지도"),
    ('📸</div><div class="tx">피드',
     '<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg></div><div class="tx">피드',
     "네비-피드"),
    ('🧭</div><div class="tx">코스',
     '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M16.24 7.76l-2.12 6.36-6.36 2.12 2.12-6.36z"/></svg></div><div class="tx">코스',
     "네비-코스"),
    ('🌐</div><div class="tx">언어',
     '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10A15.3 15.3 0 0 1 12 2z"/></svg></div><div class="tx">언어',
     "네비-언어"),
    ('👤</div><div class="tx">내 공간',
     '<svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div><div class="tx">내 공간',
     "네비-내공간"),
]
for old, new, name in nav_pairs:
    patches.append((old, new, name))

# ── 5. 로고 CSS ──
patches.append((
    '.logo{display:flex;align-items:center;gap:5px;font-size:17px;font-weight:800;color:var(--gold);flex-shrink:0}',
    '.logo{display:flex;align-items:center;gap:6px;flex-shrink:0;text-decoration:none}\n  .logo-icon{width:28px;height:28px;flex-shrink:0}\n  .logo-text{font-size:16.5px;font-weight:800;letter-spacing:-0.3px;color:var(--text)}\n  .logo-text span{color:var(--gold)}',
    "로고 CSS"
))

# ── 6. 검색바 CSS ──
patches.append((
    '.searchbar{flex:1;min-width:0;display:flex;align-items:center;gap:7px;background:var(--bg2);border-radius:22px;padding:9px 12px;border:1px solid transparent}',
    '.searchbar{flex:1;min-width:0;display:flex;align-items:center;gap:8px;background:var(--bg2);border-radius:24px;padding:9px 14px;border:1.5px solid transparent;transition:border-color .2s,background .2s,box-shadow .2s}\n  .searchbar svg{flex-shrink:0;color:var(--text3)}',
    "검색바 CSS"
))

patches.append((
    '.searchbar:focus-within{border-color:var(--gold);background:var(--white)}',
    '.searchbar:focus-within{border-color:var(--gold);background:var(--white);box-shadow:0 0 0 3px var(--gold-soft)}',
    "검색바 포커스 CSS"
))

# ── 7. 상단바 CSS gap ──
patches.append((
    '.topbar{display:flex;align-items:center;gap:6px;padding:10px 14px 10px 12px;',
    '.topbar{display:flex;align-items:center;gap:8px;padding:10px 14px 10px 14px;',
    "상단바 gap/padding"
))

# ── 적용 ──
ok = 0
skip = 0
for old, new, name in patches:
    if old in txt:
        txt = txt.replace(old, new)
        print(f"  [OK] {name}")
        ok += 1
    else:
        print(f"  [SKIP] {name}")
        skip += 1

if ok > 0:
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"\n=== {ok}개 패치 적용 완료 ===")
else:
    print("\n모든 패치가 이미 적용되어 있습니다")

# ── 검증 ──
with open(path, "r", encoding="utf-8") as f:
    check = f.read()
print("\n--- 검증 ---")
for kw in ["logo-icon", "logo-text", "backdrop-filter:blur", "oklch(0.62 0.155 65)", "v2.0.0", "gold-soft"]:
    status = "OK" if kw in check else "MISSING"
    print(f"  {kw} : {status}")
