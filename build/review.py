import json,glob,re
N=re.compile(r'[֑-ׇ]')
GEN={'bereishit':'data.json','lech':'data-lech.json'}
out=[]
for f in sorted(glob.glob('data-*.json')):
    if 'prev' in f: continue
    p=f[5:-5]
    for r in json.load(open(f)):
        hit=any(len([b for b in re.findall(r'\[([^\]]*)\]',re.sub('<[^>]+>','',e)) if len(b.split())>=12]) for e in r['e'])
        if p in('haazinu','vezot') and f"{r['c']}:{r['v']}" in '32:12 32:13 32:14 32:15 32:19 32:22 32:32 32:34 32:36 32:41 33:2 33:3 33:6 33:7 33:9 33:17 33:18 33:26'.split(): hit=True
        if not hit: continue
        out.append(f"== {p} {r['c']}:{r['v']}")
        for a,b,c in zip(r['h'],r['t'],r['e']):
            out.append(' H '+N.sub('',a)+'\n T '+N.sub('',re.sub('<[^>]+>','',b))+'\n E '+re.sub('<[^>]+>','',c))
open('review-br.txt','w').write('\n'.join(out)+'\n'); print(len([l for l in out if l.startswith('==')]))
