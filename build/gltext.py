import json,sys,re
NUM={'ראשון':1,'שני':2,'שלישי':3,'רביעי':4,'חמישי':5,'שישי':6,'שביעי':7,'מפטיר':8,'שביעי ומפטיר':7}
k=sys.argv[1]; pid,n=k.rsplit('-',1)
V=json.load(open(f'../p/{pid}.json'))['V']
on=False
for v in V:
    if v.get('a'): on = NUM[v['a']]==int(n)
    if on: print(f"{v['c']}:{v['v']}", re.sub(r'<[^>]+>','',' / '.join(v['t'])), '||', re.sub(r'<[^>]+>','',' '.join(v['e'])))
