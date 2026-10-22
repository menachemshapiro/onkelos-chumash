# Flag (word, meaning-in-pasuk) pairs whose meaning shares no content word with
# the glossary's general meaning nor with the word's Jastrow entries.
import json,glob,re,collections
from nltk.stem import PorterStemmer
from lemminflect import getAllLemmas
ps=PorterStemmer()
from functools import lru_cache
@lru_cache(None)
def norm(w):
    out={ps.stem(w)}
    for t in getAllLemmas(w).values():
        for x in t: out.add(ps.stem(x.lower()))
    return out

STOP=set("""a an the and or of to in on at by for from with as is are was were be been being it its he she they them his her their him
i me my we us our you your this that these those who whom which what there here not no will shall would should may might can could
do does did have has had let one ones into than so also lit literally same v e g cf etc pl sing masc fem
s f m ch h b q w p o n part pass af pa pe ithpa ithpe itpe el al itpa el hebrew aramaic targ y ed ib fr sq onkelos all""".split())
PART={'up','out','over','under','about','down','away','back','off','upon'}
def words(s, keep=False):
    s=re.sub(r'\(Hebrew:[^)]*\)','',s or '')     # the Hebrew's wording is not Onkelos's
    return set().union(*[norm(w) for w in re.findall(r"[a-z]+",s.lower()) if (w not in STOP or (keep and w in PART)) and len(w)>1] or [set()])
def allwords(s, keep=False): return set().union(*[norm(w) for w in re.findall(r"[a-z]+",(s or '').lower()) if (w not in STOP or (keep and w in PART)) and len(w)>1] or [set()])
ix=json.load(open('j/index.json')); E={}
for f in glob.glob('j/[A-V].json'): E.update(json.load(open(f)))
def jwords(lid):
    if lid not in ix: return None
    rid,kind,also,tabs=ix[lid]
    t=''
    for r in [rid]+list(also or []):
        if r in E: t+=' '+re.sub('<[^>]+>',' ',E[r]['html'])
    return allwords(t)
LEX={}
seen=collections.defaultdict(list)
for f in sorted(glob.glob('g/*.json')):
    pid=f[2:-5]; g=json.load(open(f)); LEX.update(g['lex'])
    items=[(None,k,v) for k,v in g['forms'].items()]+[(c,k,v) for c,d in g.get('at',{}).items() for k,v in d.items()]
    for c,k,v in items:
        l=v.get('l')
        if not l or l=='name': continue
        seen[(l,v.get('here',''))].append(f'{pid}' + (f' {c}' if c else '') + f' {k}')
out=[];nj=[]
for (l,here),where in seen.items():
    hw=words(here); hk=words(here,True)
    if not hk: continue
    gl=LEX.get(l,{}); gw=allwords(gl.get('g',''),True)
    jw=jwords(l)
    if hk & gw: continue
    if jw is not None and hw & jw: continue
    row=f"{l} | {gl.get('h','')} : {gl.get('g','')[:70]} || HERE: {here} || {'; '.join(where[:3])}{' +%d'%(len(where)-3) if len(where)>3 else ''}"
    (out if jw is not None else nj).append(row)
open('build/here-flag.txt','w').write('\n'.join(sorted(out)))
open('build/here-flag-nojas.txt','w').write('\n'.join(sorted(nj)))
print(len(seen),'pairs;',len(out),'flagged with Jastrow;',len(nj),'flagged, no Jastrow')
