import re
f=open(r'C:\Users\BRIAN MAINGI\Documents\LabelConverter\Input3\ACT WEB\donate.html','r',encoding='utf-8')
c=f.read()
f.close()
c=c.replace('counters.forEach(el => el.textContent = parseFloat(el.getAttribute(" data-target\)).toLocaleString()));','counters.forEach(el => el.textContent = parseFloat(el.getAttribute(\data-target\)).toLocaleString());')
f=open(r'C:\Users\BRIAN MAINGI\Documents\LabelConverter\Input3\ACT WEB\donate.html','w',encoding='utf-8')
f.write(c)
f.close()
print('done')
