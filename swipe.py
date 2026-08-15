# -*- coding: utf-8 -*-
import io
PATH = r"C:\Users\82102\Desktop\kstarmap\map.html"
s = io.open(PATH,"r",encoding="utf-8").read()
changes = []

old_inner = ("  inner.innerHTML =\n"
"    '<div style=\"display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid var(--border)\">' +\n"
"      '<button onclick=\"document.getElementById(\\'funBoardSheet\\').remove();setTimeout(openMoreMenu,0)\" style=\"background:var(--bg2);border:1px solid var(--border);border-radius:9px;width:36px;height:36px;font-size:18px;cursor:pointer\">\u2190</button>' +\n"
"      '<div style=\"font-size:16px;font-weight:800;flex:1\">\U0001f602 \ud55c\ub958 \uc6c3\uc74c\ucc3d\uace0</div>' +\n"
"      '<button onclick=\"openFunBoardWrite()\" style=\"background:var(--gold);color:#fff;border:none;border-radius:9px;padding:8px 14px;font-size:13px;font-weight:700;cursor:pointer\">\uae00\uc4f0\uae30</button>' +\n"
"    '</div>' +\n"
"    '<div id=\"funBoardList\" style=\"flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch\"><div style=\"padding:40px;text-align:center;color:var(--text3);font-size:13px\">\ubd88\ub7ec\uc624\ub294 \uc911...</div></div>';\n"
"  loadFunBoardList();")
new_inner = ("  inner.innerHTML =\n"
"    '<div style=\"position:relative;display:flex;align-items:center;gap:10px;padding:10px 16px;z-index:2\">' +\n"
"      '<button onclick=\"document.getElementById(\\'funBoardSheet\\').remove();setTimeout(openMoreMenu,0)\" style=\"background:rgba(0,0,0,0.4);color:#fff;border:none;border-radius:50%;width:36px;height:36px;font-size:18px;cursor:pointer\">\u2190</button>' +\n"
"      '<div style=\"font-size:15px;font-weight:800;flex:1;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,0.5)\">\U0001f602 \ud55c\ub958 \uc6c3\uc74c\ucc3d\uace0</div>' +\n"
"      '<button onclick=\"openFunBoardWrite()\" style=\"background:var(--gold);color:#fff;border:none;border-radius:9px;padding:7px 12px;font-size:12px;font-weight:700;cursor:pointer\">\uae00\uc4f0\uae30</button>' +\n"
"    '</div>' +\n"
"    '<div id=\"funSwipeWrap\" style=\"flex:1;overflow-y:auto;scroll-snap-type:y mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:none;background:#000\"><div style=\"height:100%;display:flex;align-items:center;justify-content:center;color:#888;font-size:13px\">\ubd88\ub7ec\uc624\ub294 \uc911...</div></div>';\n"
"  inner.style.cssText += 'background:#000;';\n"
"  _loadFunSwipe();")
if old_inner in s: s=s.replace(old_inner,new_inner,1); changes.append("UI")

anchor = "async function loadFunBoardList() {"
func = ("async function _loadFunSwipe() {\n"
"  const wrap = document.getElementById('funSwipeWrap');\n"
"  if (!wrap) return;\n"
"  try {\n"
"    const { db, collection, getDocs, query, orderBy, limit } = window._mapDB;\n"
"    const snap = await getDocs(query(collection(db,'funboard'), orderBy('createdAt','desc'), limit(50)));\n"
"    const posts = snap.docs.map(d => ({ id:d.id, ...d.data() }));\n"
"    if (!posts.length) { wrap.innerHTML = '<div style=\"height:100%;display:flex;align-items:center;justify-content:center;color:#888;font-size:14px\">\uc544\uc9c1 \uc601\uc0c1\uc774 \uc5c6\uc5b4\uc694.<br>\uae00\uc4f0\uae30\ub85c \uc6c3\uae34 \uc22b\uce20\ub97c \uacf5\uc720\ud574 \uc8fc\uc138\uc694!</div>'; return; }\n"
"    const ytReS = /https?:\\/\\/(?:www\\.|m\\.)?(?:youtube\\.com\\/(?:watch\\?v=|embed\\/|shorts\\/)|youtu\\.be\\/)([\\w-]{11})[^\\s]*/g;\n"
"    const allVids = [];\n"
"    posts.forEach(p => { const body=p.body||''; let m; ytReS.lastIndex=0; while((m=ytReS.exec(body))!==null) allVids.push({id:m[1],title:p.title||''}); });\n"
"    if (!allVids.length) { wrap.innerHTML = '<div style=\"height:100%;display:flex;align-items:center;justify-content:center;color:#888\">\uc601\uc0c1\uc774 \uc5c6\uc5b4\uc694</div>'; return; }\n"
"    wrap.innerHTML = allVids.map((v,i) =>\n"
"      '<div style=\"height:100%;min-height:100%;scroll-snap-align:start;display:flex;flex-direction:column;justify-content:center\">'+\n"
"        '<div data-yt=\"'+v.id+'\" onclick=\"funSwipePlay(this)\" style=\"position:relative;width:100%;max-height:80vh;aspect-ratio:9/16;margin:0 auto;cursor:pointer;background:#000;border-radius:12px;overflow:hidden\">'+\n"
"          '<img src=\"https://img.youtube.com/vi/'+v.id+'/hqdefault.jpg\" style=\"width:100%;height:100%;object-fit:cover;opacity:0.85\" loading=\"lazy\">'+\n"
"          '<div style=\"position:absolute;inset:0;display:flex;align-items:center;justify-content:center\"><div style=\"width:64px;height:64px;border-radius:50%;background:rgba(0,0,0,0.6);display:flex;align-items:center;justify-content:center\"><div style=\"width:0;height:0;border-top:12px solid transparent;border-bottom:12px solid transparent;border-left:20px solid #fff;margin-left:4px\"></div></div></div>'+\n"
"        '</div>'+\n"
"        (v.title?'<div style=\"text-align:center;color:#ddd;font-size:12px;margin-top:8px;padding:0 20px\">'+v.title.replace(/</g,'&lt;')+'</div>':'')+\n"
"        '<div style=\"text-align:center;color:#666;font-size:11px;margin-top:4px\">'+(i+1)+'/'+allVids.length+'</div>'+\n"
"      '</div>'\n"
"    ).join('');\n"
"  } catch(e) { console.error(e); }\n"
"}\n"
"window.funSwipePlay = function(el) {\n"
"  const id = el.getAttribute('data-yt');\n"
"  el.outerHTML = '<div style=\"width:100%;max-height:80vh;aspect-ratio:9/16;margin:0 auto;border-radius:12px;overflow:hidden\"><iframe src=\"https://www.youtube.com/embed/'+id+'?autoplay=1\" style=\"width:100%;height:100%;border:0\" allowfullscreen allow=\"autoplay;encrypted-media\"></iframe></div>';\n"
"};\n")
if anchor in s and "_loadFunSwipe" not in s: s=s.replace(anchor,func+anchor,1); changes.append("func")

s=s.replace("const VERSION = 'map v1.9.25';","const VERSION = 'map v1.9.26';"); changes.append("v1.9.26")
io.open(PATH,"w",encoding="utf-8",newline="").write(s)
print("OK -", ", ".join(changes))
