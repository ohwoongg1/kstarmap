f=open('map.html','r',encoding='utf-8');t=f.read();f.close()
c=0

t2=t.replace(
    'position:fixed;inset:0;z-index:9999;display:flex;justify-content:center;background:rgba(0,0,0,0.3)',
    'position:fixed;inset:0;z-index:9999;display:flex;justify-content:center;background:rgba(0,0,0,0.3);overscroll-behavior:none'
)
if t2!=t: c+=1; t=t2; print('[OK] boardSheet overscroll:none')

t2=t.replace(
    'position:fixed;inset:0;z-index:10000;display:flex;justify-content:center;background:rgba(0,0,0,0.3)',
    'position:fixed;inset:0;z-index:10000;display:flex;justify-content:center;background:rgba(0,0,0,0.3);overscroll-behavior:none'
)
if t2!=t: c+=1; t=t2; print('[OK] boardWrite overscroll:none')

t2=t.replace(
    'id="boardList" style="flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch"',
    'id="boardList" style="flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain"'
)
if t2!=t: c+=1; t=t2; print('[OK] boardList contain')

t=t.replace("map v2.3.5","map v2.3.6")
f=open('map.html','w',encoding='utf-8');f.write(t);f.close()
print('total:',c)
