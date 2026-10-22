# Flag word-by-word pairs where the Onkelos English for an Aramaic word shares nothing with
# that word's glossary meaning (in this pasuk or in general) or its Jastrow entry.
import json,glob,re,sys,unicodedata,collections
sys.path.insert(0,'build')
import importlib.util
spec=importlib.util.spec_from_file_location('hc','build/here_check.py')
src=open('build/here_check.py').read().split('LEX={}')[0]   # reuse helpers only
exec(src)
N=lambda s:unicodedata.normalize('NFC',s)
from nltk.corpus import wordnet as wn
SPELL={'shabbos':'sabbath','mon':'manna','amohs':'cubits','amoh':'cubit','matzoh':'matzah','matzos':'matzah','shechina':'shechinah presence',
'tefach':'handbreadth','adonoy':'hashem','elokim':'god','elohim':'god','bnei':'sons','yisroel':'israel','kohen':'priest','kohanim':'priests',
'levi':'levite','leviim':'levites','mishkan':'tabernacle sanctuary','succos':'booths','pesach':'passover','olah':'burnt','minchah':'meal grain offering',
'shelamim':'peace','chatas':'sin','asham':'guilt','toras':'law','torah':'law','selaim':'sela','sela':'sela','kohein':'priest','kohanim':'priest','nei':'sons','b':'','shekalim':'shekel','shekels':'shekel','tamid':'continual','omer':'omer','kodesh':'holy','kodshim':'holy'}
@lru_cache(None)
def syn(w):
    out=set(norm(w))
    for x in SPELL.get(w,'').split(): out|=norm(x)
    for ss in wn.synsets(w)[:8]:
        for l in ss.lemmas():
            for t in l.name().lower().split('_'): out|=norm(t)
            for d in l.derivationally_related_forms():
                for t in d.name().lower().split('_'): out|=norm(t)
        for sim in ss.similar_tos():
            for l in sim.lemmas(): out|=norm(l.name().lower())
    return frozenset(out)
def swords(s):
    return set().union(*[syn(w) for w in re.findall(r"[a-z]+",s.lower()) if w not in STOP and len(w)>1] or [set()])
out=[];n=0
for f in sorted(glob.glob('p/*.json')):
    pid=f[2:-5]
    try: g=json.load(open(f'g/{pid}.json'))
    except: continue
    F={N(k):v for k,v in g['forms'].items()}; AT={c:{N(k):v for k,v in d.items()} for c,d in g.get('at',{}).items()}
    for v in json.load(open(f))['V']:
        if not v.get('ea'): continue
        cv=f"{v['c']}:{v['v']}"
        for cl in v['ea']:
            if not cl: continue
            for a,e in cl.get('map',[]):
                if not e or not re.search('[A-Za-z]',e): continue
                fm=AT.get(cv,{}).get(N(a)) or F.get(N(a))
                if not fm or fm.get('l') in (None,'name','ednote','yy','yat'): continue
                n+=1
                ew=swords(e)
                if not ew: continue
                lx=g['lex'].get(fm['l'],{})
                if ew & swords(re.sub(r'\(Hebrew:[^)]*\)','',fm.get('here',''))): continue
                if ew & swords(lx.get('g','')): continue
                jw=jwords(fm['l'])
                if jw and ew & jw: continue
                out.append(f"{pid} {cv} | {a} = \"{e}\" || here: {fm.get('here','')} || {fm['l']}: {lx.get('g','')[:60]}")
G=collections.OrderedDict()
for r in out:
    loc,rest=r.split(' | ',1); G.setdefault(rest,[]).append(loc)
rows=[f"{k} || {'; '.join(v[:3])}{' +%d'%(len(v)-3) if len(v)>3 else ''}" for k,v in G.items()]
open('build/eo-flag.txt','w').write('\n'.join(rows)); print(n,'pairs checked;',len(out),'flagged;',len(rows),'unique')
