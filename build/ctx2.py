# ctx2.py N FORM... : up to N occurrences per form (spread across the Torah), with Aramaic window and English
import json, re, sys, unicodedata as u
N=lambda x:u.normalize('NFC',x)
n=int(sys.argv[1]); want=[N(w) for w in sys.argv[2:]]
V={}
def verse(p,cv):
    if p not in V: V[p]={f"{x['c']}:{x['v']}":(re.sub('<[^>]+>','',' '.join(x['t'])),re.sub('<[^>]+>','',' '.join(x['e']))) for x in json.load(open(f'../p/{p}.json'))['V']}
    return V[p].get(cv,('',''))
occ={w:[] for w in want}
for r in open('all-gloss.tsv'):
    f=r.rstrip('\n').split('\t')
    if N(f[2]) in occ: occ[N(f[2])].append(f)
for w in want:
    L=occ[w]
    if not L: continue
    step=max(1,len(L)//n); pick=L[::step][:n]
    print(f'## {w} ({len(L)}) form-gloss: {L[0][5] if L[0][3]=="form" else "-"}')
    for f in pick:
        t,e=verse(f[0],f[1]); ws=t.split(); i=next((k for k,x in enumerate(ws) if N(x).startswith(w)),0)
        print(f'  {f[3][0]} {f[0]} {f[1]} [{f[5]}] {" ".join(ws[max(0,i-2):i+3])} || {e[:90]}')
