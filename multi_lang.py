# -*- coding: utf-8 -*-
import io
PATH = r"C:\Users\82102\Desktop\kstarmap\map.html"
s = io.open(PATH, "r", encoding="utf-8").read()

# A안: 아시아권(ko,ja,zh,zh-TW,th,vi,id)만 모국어 "촬영지" 키워드.
# 나머지(en,es,fr,ru,ar)는 매핑에 없으므로 기본값 en('filming location') 사용.
old_q = "        const _q = _isEnDisp ? ('\"' + _mt + '\" filming location') : ('\"' + _mt + '\" \uCD2C\uC601\uC9C0');"

if old_q not in s:
    print("ERROR: _q line not found"); raise SystemExit
if "_LOC_KW" in s:
    print("SKIP: already applied"); raise SystemExit

new_q = "\n".join([
"        const _LOC_KW = {ko:'\uCD2C\uC601\uC9C0', ja:'\u30ED\u30B1\u5730', zh:'\u53D6\u666F\u5730', 'zh-TW':'\u62CD\u651D\u5730', id:'lokasi syuting', th:'\u0E2A\u0E16\u0E32\u0E19\u0E17\u0E35\u0E48\u0E16\u0E48\u0E32\u0E22\u0E17\u0E33', vi:'\u0111\u1ECBa \u0111i\u1EC3m quay phim'};",
"        const _kw = _LOC_KW[_dispLang] || 'filming location';",
"        const _q = '\"' + _mt + '\" ' + _kw;",
])

s = s.replace(old_q, new_q)
s = s.replace("const VERSION = 'map v1.9.4';", "const VERSION = 'map v1.9.5';")
io.open(PATH, "w", encoding="utf-8", newline="").write(s)
print("OK - Asian-language location keywords applied (A plan)")
