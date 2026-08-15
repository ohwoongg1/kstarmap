old=open('old_map.html','r',encoding='utf-8-sig').read()
new=open('map.html','r',encoding='utf-8').read()
for label,t in [('OLD',old),('NEW',new)]:
    i=t.find('html,body{')
    if i>0: print(f'{label}: {t[i:i+200]}')
for label,t in [('OLD',old),('NEW',new)]:
    i=t.find('#mapWrap')
    if i>0: print(f'{label} mapWrap: {t[i:i+300]}')
