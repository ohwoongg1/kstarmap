# Phase 1 보충 패치 — 상단바 HTML + 하단 네비 HTML
# PowerShell here-string 매칭 문제 우회: 정규식 기반
$file = "C:\Users\82102\Desktop\kstarmap\map.html"
$txt = [IO.File]::ReadAllText($file, [Text.Encoding]::UTF8)
$count = 0

# ── 1. 로고 교체: <div class="logo">⭐ KStar</div> → SVG 로고 ──
$oldLogo = '<div class="logo">⭐ KStar</div>'
$newLogo = @'
<div class="logo">
      <svg class="logo-icon" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="16" cy="16" r="15" fill="oklch(0.62 0.155 65)"/>
        <path d="M16 7l2.47 5.76L24.5 13.5l-4.5 4 1.27 6L16 20.5l-5.27 3 1.27-6-4.5-4 6.03-.74Z" fill="#fff"/>
      </svg>
      <div class="logo-text">K<span>Star</span>Map</div>
    </div>
'@
if ($txt.Contains($oldLogo)) {
  $txt = $txt.Replace($oldLogo, $newLogo)
  Write-Host "[OK] 로고 SVG 교체" -ForegroundColor Green
  $count++
} else {
  Write-Host "[SKIP] 로고 - 이미 적용됨" -ForegroundColor Yellow
}

# ── 2. 검색바 아이콘: 🔍 span → SVG ──
$oldSearch = '<span style="font-size:15px;color:var(--text3)">🔍</span>'
$newSearch = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35"/></svg>'
if ($txt.Contains($oldSearch)) {
  $txt = $txt.Replace($oldSearch, $newSearch)
  Write-Host "[OK] 검색 아이콘 SVG 교체" -ForegroundColor Green
  $count++
} else {
  Write-Host "[SKIP] 검색 아이콘 - 이미 적용됨" -ForegroundColor Yellow
}

# ── 3. 햄버거 버튼: 빨간 배경 → gold SVG ──
$oldBtn = 'style="flex-shrink:0;background:#c0392b;border:1px solid #a93226;border-radius:8px;padding:6px 7px;font-size:14px;font-weight:700;color:#fff;cursor:pointer">☰</button>'
$newBtn = 'style="flex-shrink:0;background:var(--gold);border:none;border-radius:10px;padding:7px 8px;cursor:pointer;display:flex;align-items:center;justify-content:center" aria-label="메뉴"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>'
if ($txt.Contains($oldBtn)) {
  $txt = $txt.Replace($oldBtn, $newBtn)
  Write-Host "[OK] 햄버거 버튼 교체" -ForegroundColor Green
  $count++
} else {
  Write-Host "[SKIP] 햄버거 버튼 - 이미 적용됨" -ForegroundColor Yellow
}

# ── 4. 하단 네비: 이모지 → SVG (각 탭 개별 교체) ──
# 지도
$txt = $txt.Replace(
  '<div class="ic">🗺️</div><div class="tx">지도</div>',
  '<div class="ic"><svg viewBox="0 0 24 24"><path d="M9 2L3 5v17l6-3 6 3 6-3V2l-6 3-6-3z"/><path d="M9 2v17M15 5v17"/></svg></div><div class="tx">지도</div>'
)
# 피드
$txt = $txt.Replace(
  '<div class="ic">📸</div><div class="tx">피드</div>',
  '<div class="ic"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg></div><div class="tx">피드</div>'
)
# 코스
$txt = $txt.Replace(
  '<div class="ic">🧭</div><div class="tx">코스</div>',
  '<div class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M16.24 7.76l-2.12 6.36-6.36 2.12 2.12-6.36z"/></svg></div><div class="tx">코스</div>'
)
# 언어
$txt = $txt.Replace(
  '<div class="ic">🌐</div><div class="tx">언어</div>',
  '<div class="ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10A15.3 15.3 0 0 1 12 2z"/></svg></div><div class="tx">언어</div>'
)
# 내 공간
$txt = $txt.Replace(
  '<div class="ic">👤</div><div class="tx">내 공간</div>',
  '<div class="ic"><svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div><div class="tx">내 공간</div>'
)
Write-Host "[OK] 하단 네비 5개 탭 SVG 교체" -ForegroundColor Green
$count++

# ── 5. 상단바 CSS 보충 (logo-icon, logo-text 클래스 추가) ──
$oldTopCSS = '.logo{display:flex;align-items:center;gap:5px;font-size:17px;font-weight:800;color:var(--gold);flex-shrink:0}'
$newTopCSS = @'
.logo{display:flex;align-items:center;gap:6px;flex-shrink:0;text-decoration:none}
  .logo-icon{width:28px;height:28px;flex-shrink:0}
  .logo-text{font-size:16.5px;font-weight:800;letter-spacing:-0.3px;color:var(--text)}
  .logo-text span{color:var(--gold)}
'@
if ($txt.Contains($oldTopCSS)) {
  $txt = $txt.Replace($oldTopCSS, $newTopCSS)
  Write-Host "[OK] 로고 CSS 추가" -ForegroundColor Green
  $count++
} else {
  Write-Host "[SKIP] 로고 CSS - 이미 적용됨" -ForegroundColor Yellow
}

# ── 6. 검색바 CSS 보충 (glow 효과) ──
$oldSbCSS = '.searchbar{flex:1;min-width:0;display:flex;align-items:center;gap:7px;background:var(--bg2);border-radius:22px;padding:9px 12px;border:1px solid transparent}'
$newSbCSS = '.searchbar{flex:1;min-width:0;display:flex;align-items:center;gap:8px;background:var(--bg2);border-radius:24px;padding:9px 14px;border:1.5px solid transparent;transition:border-color .2s,background .2s,box-shadow .2s}'
if ($txt.Contains($oldSbCSS)) {
  $txt = $txt.Replace($oldSbCSS, $newSbCSS)
  Write-Host "[OK] 검색바 CSS" -ForegroundColor Green
  $count++
} else {
  Write-Host "[SKIP] 검색바 CSS - 이미 적용됨" -ForegroundColor Yellow
}

$oldSbFocus = '.searchbar:focus-within{border-color:var(--gold);background:var(--white)}'
$newSbFocus = '.searchbar:focus-within{border-color:var(--gold);background:var(--white);box-shadow:0 0 0 3px var(--gold-soft)}'
if ($txt.Contains($oldSbFocus)) {
  $txt = $txt.Replace($oldSbFocus, $newSbFocus)
  Write-Host "[OK] 검색바 포커스 CSS" -ForegroundColor Green
  $count++
} else {
  Write-Host "[SKIP] 검색바 포커스 - 이미 적용됨" -ForegroundColor Yellow
}

# ── 저장 + 배포 ──
if ($count -gt 0) {
  [IO.File]::WriteAllText($file, $txt, (New-Object Text.UTF8Encoding $true))
  Write-Host "`n=== $count 개 보충 패치 적용 ===" -ForegroundColor Cyan
  Set-Location "C:\Users\82102\Desktop\kstarmap"
  git add map.html
  git commit -m "v2.0.0 Phase 1 fix: logo SVG, search icon, nav icons, menu button"
  git push
  Write-Host "`nCloudflare > Purge Everything + Ctrl+Shift+R" -ForegroundColor Magenta
} else {
  Write-Host "`n모든 패치가 이미 적용되어 있습니다" -ForegroundColor Green
}

# ── 최종 검증 ──
$f2 = [IO.File]::ReadAllText($file, [Text.Encoding]::UTF8)
Write-Host "`n--- 검증 ---" -ForegroundColor Cyan
@("logo-icon", "logo-text", "backdrop-filter:blur", "oklch(0.62 0.155 65)", "v2.0.0") | ForEach-Object {
  "$_ : $(if($f2.Contains($_)){'OK'}else{'MISSING'})"
}
