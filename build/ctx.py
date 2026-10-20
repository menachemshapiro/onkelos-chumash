# ctx.py FORM... : each occurrence of a form with its gloss, Aramaic window and English (trimmed)
import json, re, sys, unicodedata as u
N=lambda x:u.normalize('NFC',x)
want={N(w) for w in sys.argv[1:]}
V={}
def verse(p,cv):
    if p not in V: V[p]={f"{x['c']}:{x['v']}":(re.sub('<[^>]+>','',' '.join(x['t'])),re.sub('<[^>]+>','',' '.join(x['e']))) for x in json.load(open(f'../p/{p}.json'))['V']}
    return V[p].get(cv,('',''))
for r in open('all-gloss.tsv'):
    f=r.rstrip('\n').split('\t')
    if N(f[2]) not in want: continue
    t,e=verse(f[0],f[1]); ws=t.split(); i=next((k for k,w in enumerate(ws) if N(w).startswith(N(f[2]))),0)
    print(f'{f[2]}|{f[3][0]}|{f[5]}|{f[0]} {f[1]}|{" ".join(ws[max(0,i-2):i+3])}|{e[:110]}')
