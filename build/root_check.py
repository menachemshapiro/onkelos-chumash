# Flag forms whose stem lacks the strong letters of their word's root (a sign of a wrong link).
import json,glob,re,collections,unicodedata
def cons(s): return re.sub(r'[^א-ת]','',unicodedata.normalize('NFD',s or ''))
FIN=str.maketrans('ךםןףץ','כמנפצ')
EQ=str.maketrans('ס','ש')
WEAK=set('אהוינ')
def strong(r):
    o=[]
    for c in cons(r).translate(FIN).translate(EQ):
        if c not in WEAK and (not o or o[-1]!=c): o.append(c)
    return o
def insub(need,s):
    it=iter(s); return all(c in it for c in need)
out=collections.defaultdict(list); LEX={}
for f in sorted(glob.glob('g/*.json')):
    pid=f[2:-5]; g=json.load(open(f)); LEX.update(g['lex'])
    items=[(None,k,v) for k,v in g['forms'].items()]+[(c,k,v) for c,d in g.get('at',{}).items() for k,v in d.items()]
    for c,k,v in items:
        l=v.get('l')
        if not l or l in('name','ednote'): continue
        r=g['lex'].get(l,{}).get('r','') or LEX.get(l,{}).get('r','')
        need=strong(r)
        if len(need)<2: continue
        s=cons(k).translate(FIN).translate(EQ)
        if not insub(need,s): out[(l,r,g['lex'].get(l,{}).get('g','')[:50])].append(f"{pid}{' '+c if c else ''} {k} = {v.get('here','')}")
rows=[f"{l} [{r}] {g} || "+' ; '.join(w[:3])+(f' +{len(w)-3}' if len(w)>3 else '') for (l,r,g),w in sorted(out.items())]
open('build/root-flag.txt','w').write('\n'.join(rows)); print(len(rows))
