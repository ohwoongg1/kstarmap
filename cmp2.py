old=open('before230.html','r',encoding='utf-8-sig').read()
new=open('map.html','r',encoding='utf-8').read()
import re
for tag in ['#app','#mapWrap','#sidePanel','#railNav','@media','min-width:900','boardSheet']:
    print(f'=== {tag} ===')
    for label,t in [('BEFORE',old),('NOW',new)]:
        lines=[l.strip() for l in t.split('\n') if tag in l]
        for l in lines[:3]: print(f'  {label}: {l[:150]}')
    print()
