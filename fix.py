f=open('map.html','r',encoding='utf-8');t=f.read();f.close()
old='width:480px;flex-shrink:0'
new='width:620px;flex-shrink:0'
if old in t:
    t=t.replace(old,new)
    t=t.replace("map v2.3.4","map v2.3.5")
    f=open('map.html','w',encoding='utf-8');f.write(t);f.close()
    print('OK: 480->620 + v2.3.5')
else:
    print('FAIL: 480px not found')
