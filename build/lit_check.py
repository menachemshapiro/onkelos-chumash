import json,glob,re,os
def cons(s): return re.sub(r'[^א-ת]','',s)
ix=json.load(open('j/index.json')); E={}
for f in glob.glob('j/[A-V].json'): E.update(json.load(open(f)))
def jg(rid):
    h=re.sub('<[^>]+>','',E[rid]['html']); return E[rid]['h']+' :: '+re.sub(r'\s+',' ',h)[:230]
for fn in sorted(glob.glob('build/eo-align/*.txt')):
    pid=os.path.basename(fn)[:-4].split("-")[0]
    try: g=json.load(open(f'g/{pid}.json'))
    except: continue
    F=g['forms']; L=g['lex']; FC={}
    for k,v in F.items(): FC.setdefault(cons(k),v)
    v='?'
    for line in open(fn,encoding='utf8'):
        if line.startswith('@'): v=line[1:].strip()
        if line.startswith('!') and 'literally' in line:
            for m in re.finditer(r'([֐-׿][֐-׿\s־]*?)\s+(?:is|means)\s+literally\s+"([^"]+)"',line):
                w=m.group(1).strip().split()[-1]; f=F.get(w) or FC.get(cons(w))
                lid=f['l'] if f else None
                lx=L.get(lid,{}) if lid else {}
                print(f'{pid} {v} | {w} = "{m.group(2)}" | lex {lid}: {lx.get("g","")[:70]}')
                if lid in ix: print('   J', jg(ix[lid][0]))
                else: print('   J none')
