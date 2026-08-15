f=open('map.html','r',encoding='utf-8');t=f.read();f.close()
old='#appMain{display:flex;flex-direction:column;flex:1;min-height:0;min-width:0}'
new='#appMain{display:flex;flex-direction:column;flex:1;min-height:0;min-width:0;overflow:hidden}'
t=t.replace(old,new).replace("map v2.3.8","map v2.3.9")
f=open('map.html','w',encoding='utf-8');f.write(t);f.close()
print('OK' if new in t else 'FAIL')
