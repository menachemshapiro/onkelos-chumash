# poly.py : shared glosses whose key word rarely shows up in the verse's English -> poly2.txt
import json,re,unicodedata as u
from collections import defaultdict
N=lambda x:u.normalize('NFC',x)
EN={}
def en(p,cv):
    if p not in EN: EN[p]={f"{x['c']}:{x['v']}":re.sub('<[^>]+>','',' '.join(x['e'])).lower() for x in json.load(open(f'../p/{p}.json'))['V']}
    return EN[p].get(cv,'')
STOP=set('the and that which from with into upon unto this these those their there them they shall will would have been being were your yours ours hers about lit. like before after over under among also'.split())
def kw(h):
    h=re.sub(r'\([^)]*\)','',h).lower()
    return [w for w in re.findall(r"[a-z]+",h) if len(w)>=4 and w not in STOP]
done=set()
for l in open('gl/cleanup.txt'):
    s=l.strip()
    if not s or s.startswith('#'): continue
    s=re.sub(r'^(~\S+?>)?([a-z]+/)?(\d+:\d+>)?','',s.split('|')[0].strip())
    done.add(N(''.join(re.split(r'[=~]',x)[0] for x in re.split(r'\.(?=[֑-ת◌־])',s))))
occ=defaultdict(list)
for r in open('all-gloss.tsv'):
    f=r.rstrip('\n').split('\t')
    if f[3]!='form' or N(f[2]) in done: continue
    ws=kw(f[5])
    if not ws: continue
    occ[(f[2],f[5])].append(any(w[:4] in en(f[0],f[1]) for w in ws))
rows=[]
for (t,h),v in occ.items():
    n=len(v); k=sum(v)
    if n>=3 and k/n<0.4 and not re.match(r'^((the|of|to|in|and|from) )*[A-Z]',h) and 'Hashem' not in h: rows.append((n-k,n,t,h))
rows.sort(key=lambda x:-x[0])
open('poly2.txt','w').write(''.join(f'{a}/{b}\t{t}\t{h}\n' for a,b,t,h in rows))
print(len(rows))
