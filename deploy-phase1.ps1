# KStarMap Phase 1 Deploy Script (v2.0.0)
# 사용법: PowerShell에서 이 파일을 실행
# cd C:\Users\82102\Desktop\kstarmap
# .\deploy-phase1.ps1

$file = "C:\Users\82102\Desktop\kstarmap\map.html"
$txt = [IO.File]::ReadAllText($file, [Text.Encoding]::UTF8)

# ── 1. 색상 시스템: oklch 전환 ──
$old1 = @"
  :root{
    --bg:#ffffff; --bg2:#f5f4ef; --white:#ffffff;
    --text:#1a1a1a; --text2:#4a4a48; --text3:#8a8a85;
    --border:#e6e4dc; --border2:#cfcdc4;
    --gold:#B5790F; --gold-bg:rgba(181,121,15,0.1);
    --red:#E24B4A; --blue:#378ADD; --amber:#EF9F27;
    --shadow:0 2px 10px rgba(0,0,0,0.12);
  }
"@
$new1 = @"
  :root{
    /* ── oklch color system ── */
    --bg:oklch(1.00 0 0); --bg2:oklch(0.965 0.006 85); --white:oklch(1.00 0 0);
    --text:oklch(0.16 0.01 250); --text2:oklch(0.38 0.01 250); --text3:oklch(0.58 0.008 250);
    --border:oklch(0.905 0.006 85); --border2:oklch(0.835 0.008 85);
    --gold:oklch(0.62 0.155 65); --gold-bg:oklch(0.62 0.155 65 / 0.1);
    --gold-soft:oklch(0.62 0.155 65 / 0.08);
    --red:oklch(0.60 0.19 25); --blue:oklch(0.60 0.14 250); --amber:oklch(0.74 0.155 75);
    --shadow:0 2px 12px oklch(0.16 0.01 250 / 0.10);
    /* nav */
    --nav-inactive:oklch(0.55 0.01 250);
    --nav-active:oklch(0.62 0.155 65);
    --nav-bg:oklch(1.00 0 0 / 0.85);
  }
"@

# ── 2. 상단바 CSS ──
$old2 = @"
  /* 상단바 */
  .topbar{display:flex;align-items:center;gap:6px;padding:10px 14px 10px 12px;background:var(--bg);border-bottom:0.5px solid var(--border);flex-shrink:0;z-index:30}
  .logo{display:flex;align-items:center;gap:5px;font-size:17px;font-weight:800;color:var(--gold);flex-shrink:0}
  .searchbar{flex:1;min-width:0;display:flex;align-items:center;gap:7px;background:var(--bg2);border-radius:22px;padding:9px 12px;border:1px solid transparent}
  .searchbar:focus-within{border-color:var(--gold);background:var(--white)}
  .searchbar input{flex:1;border:none;outline:none;background:none;font-size:14px;color:var(--text)}
  .searchbar input::placeholder{color:var(--text3)}
"@
$new2 = @"
  /* 상단바 */
  .topbar{display:flex;align-items:center;gap:8px;padding:10px 14px 10px 14px;background:var(--bg);border-bottom:0.5px solid var(--border);flex-shrink:0;z-index:30}
  .logo{display:flex;align-items:center;gap:6px;flex-shrink:0;text-decoration:none}
  .logo-icon{width:28px;height:28px;flex-shrink:0}
  .logo-text{font-size:16.5px;font-weight:800;letter-spacing:-0.3px;color:var(--text)}
  .logo-text span{color:var(--gold)}
  .searchbar{flex:1;min-width:0;display:flex;align-items:center;gap:8px;background:var(--bg2);border-radius:24px;padding:9px 14px;border:1.5px solid transparent;transition:border-color .2s,background .2s,box-shadow .2s}
  .searchbar:focus-within{border-color:var(--gold);background:var(--white);box-shadow:0 0 0 3px var(--gold-soft)}
  .searchbar svg{flex-shrink:0;color:var(--text3)}
  .searchbar input{flex:1;border:none;outline:none;background:none;font-size:14px;color:var(--text)}
  .searchbar input::placeholder{color:var(--text3)}
"@

# ── 3. 하단 탭 CSS ──
$old3 = @"
  /* 하단 탭 */
  .bottomnav{display:flex;background:var(--bg);border-top:0.5px solid var(--border);flex-shrink:0;padding-bottom:env(safe-area-inset-bottom);position:relative;z-index:40}
  .navtab{flex:1;text-align:center;padding:9px 0 8px;cursor:pointer;color:var(--text3)}
  .navtab.active{color:var(--gold)}
  .navtab .ic{font-size:20px;line-height:1}
  .navtab .tx{font-size:10.5px;margin-top:3px;font-weight:600}
"@
$new3 = @"
  /* 하단 탭 */
  .bottomnav{display:flex;background:var(--nav-bg);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-top:0.5px solid var(--border);flex-shrink:0;padding-bottom:env(safe-area-inset-bottom);position:relative;z-index:40}
  .navtab{flex:1;display:flex;flex-direction:column;align-items:center;padding:8px 0 7px;cursor:pointer;color:var(--nav-inactive);transition:color .2s;position:relative;-webkit-tap-highlight-color:transparent}
  .navtab.active{color:var(--nav-active)}
  .navtab .ic{width:24px;height:24px;display:flex;align-items:center;justify-content:center}
  .navtab .ic svg{width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;transition:stroke-width .15s}
  .navtab.active .ic svg{stroke-width:2.2}
  .navtab .tx{font-size:10px;margin-top:3px;font-weight:600;letter-spacing:-0.1px}
  .navtab.active::after{content:'';position:absolute;top:2px;left:50%;transform:translateX(-50%);width:4px;height:4px;border-radius:50%;background:var(--nav-active)}
"@

# ── 4. 상단바 HTML (로고 + 검색바 + 메뉴 버튼) ──
$old4 = @"
    <div class="logo">⭐ KStar</div>
    <div class="searchbar">
      <span style="font-size:15px;color:var(--text3)">🔍</span>
      <input id="searchInput" type="text" placeholder="장소·주소 검색 (예: 중앙고등학교)" autocomplete="off">
      <span id="searchClear" style="display:none;font-size:16px;color:var(--text3);cursor:pointer">✕</span>
    </div>
    <button id="langToggle" onclick="openMoreMenu()" style="flex-shrink:0;background:#c0392b;border:1px solid #a93226;border-radius:8px;padding:6px 7px;font-size:14px;font-weight:700;color:#fff;cursor:pointer">☰</button>
"@
$new4 = @"
    <div class="logo">
      <svg class="logo-icon" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="16" r="15" fill="oklch(0.62 0.155 65)"/>
        <path d="M16 7l2.47 5.76L24.5 13.5l-4.5 4 1.27 6L16 20.5l-5.27 3 1.27-6-4.5-4 6.03-.74Z" fill="#fff"/>
      </svg>
      <div class="logo-text">K<span>Star</span>Map</div>
    </div>
    <div class="searchbar">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35"/></svg>
      <input id="searchInput" type="text" placeholder="장소·주소 검색 (예: 중앙고등학교)" autocomplete="off">
      <span id="searchClear" style="display:none;font-size:16px;color:var(--text3);cursor:pointer">✕</span>
    </div>
    <button id="langToggle" onclick="openMoreMenu()" style="flex-shrink:0;background:var(--gold);border:none;border-radius:10px;padding:7px 8px;cursor:pointer;display:flex;align-items:center;justify-content:center" aria-label="메뉴">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
"@

# ── 5. 하단 네비게이션 HTML ──
$old5 = @"
  <div class="bottomnav">
    <div class="navtab active" onclick="switchTab('map')"><div class="ic">🗺️</div><div class="tx">지도</div></div>
    <div class="navtab" onclick="switchTab('feed')"><div class="ic">📸</div><div class="tx">피드</div></div>
    <div class="navtab" onclick="switchTab('course')"><div class="ic">🧭</div><div class="tx">코스</div></div>
    <div class="navtab" onclick="openLangPicker()"><div class="ic">🌐</div><div class="tx">언어</div></div>
    <div class="navtab" onclick="switchTab('my')"><div class="ic">👤</div><div class="tx">내 공간</div></div>
  </div>
"@
$new5 = @"
  <div class="bottomnav">
    <div class="navtab active" onclick="switchTab('map')">
      <div class="ic"><svg viewBox="0 0 24 24"><path d="M9 2L3 5v17l6-3 6 3 6-3V2l-6 3-6-3z"/><path d="M9 2v17M15 5v17"/></svg></div>
      <div class="tx">지도</div>
    </div>
    <div class="navtab" onclick="switchTab('feed')">
      <div class="ic"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg></div>
      <div class="tx">피드</div>
    </div>
    <div class="navtab" onclick="switchTab('course')">
      <div class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M16.24 7.76l-2.12 6.36-6.36 2.12 2.12-6.36z"/></svg></div>
      <div class="tx">코스</div>
    </div>
    <div class="navtab" onclick="openLangPicker()">
      <div class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10A15.3 15.3 0 0 1 12 2z"/></svg></div>
      <div class="tx">언어</div>
    </div>
    <div class="navtab" onclick="switchTab('my')">
      <div class="ic"><svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
      <div class="tx">내 공간</div>
    </div>
  </div>
"@

# ── 6. 버전 ──
$old6 = "const VERSION = 'map v1.9.59';"
$new6 = "const VERSION = 'map v2.0.0';"

# ── 적용 ──
$pairs = @(
  @($old1, $new1, "색상 시스템 oklch"),
  @($old2, $new2, "상단바 CSS"),
  @($old3, $new3, "하단탭 CSS"),
  @($old4, $new4, "상단바 HTML"),
  @($old5, $new5, "하단 네비 HTML"),
  @($old6, $new6, "버전")
)

$ok = 0; $fail = 0
foreach ($p in $pairs) {
  if ($txt.Contains($p[0])) {
    $txt = $txt.Replace($p[0], $p[1])
    Write-Host "[OK] $($p[2])" -ForegroundColor Green
    $ok++
  } else {
    Write-Host "[SKIP] $($p[2]) - 매칭 안됨 (이미 적용?)" -ForegroundColor Yellow
    $fail++
  }
}

if ($ok -gt 0) {
  [IO.File]::WriteAllText($file, $txt, (New-Object Text.UTF8Encoding $true))
  Write-Host "`n=== $ok 개 패치 적용 완료 (v2.0.0) ===" -ForegroundColor Cyan
} else {
  Write-Host "`n모든 패치가 이미 적용되었거나 매칭 실패" -ForegroundColor Yellow
}

if ($fail -gt 0) {
  Write-Host "$fail 개 항목이 매칭되지 않았습니다. 파일을 확인해 주세요." -ForegroundColor Yellow
}

# ── 배포 ──
Write-Host "`n--- git 배포 ---" -ForegroundColor Cyan
Set-Location "C:\Users\82102\Desktop\kstarmap"
git add map.html
git commit -m "v2.0.0 Phase 1: oklch colors, SVG logo, searchbar glow, bottom nav redesign"
git push

Write-Host "`n배포 후 Cloudflare > Purge Everything + Ctrl+Shift+R 잊지 마세요!" -ForegroundColor Magenta
