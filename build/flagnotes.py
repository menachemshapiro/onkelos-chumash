"""flagnotes.py PARSHA... : list word-by-word pairs where Metsudah's kept English (not bold) shares no content word
with the glossary meaning of its Aramaic word. Candidates for a note; most will be harmless synonyms."""
import json, re, sys, unicodedata as u
N=lambda s:u.normalize('NFC',s)
STOP=set("a an the of to in on at by for from with and or but is are was were be been being it its his her their them they he she him you your we our us i me my this that these those who whom which what as so not no do does did shall will would should may might can could there here up out into upon over under all one ones has have had let lo".split())
def stem(w):
    w=w.lower().strip("’'")
    for suf in ('ings','ing','edly','ed','es','s','ly'):
        if len(w)>4 and w.endswith(suf): return w[:-len(suf)]
    return w
def content(s): return {stem(w) for w in re.findall(r"[A-Za-z’']+", re.sub(r'\([^)]*\)','',s)) if w.lower() not in STOP}
def bare(s): return re.sub(r'\{[^}]*\}',' ',re.sub(r'<b>.*?</b>',' ',s))
for arg in sys.argv[1:]:
    ef, pid = (arg.split(':') + [arg])[:2]
    # glosses from the worksheet
    gl={}; cur=None
    for l in open(f'ws-full/{pid}.txt',encoding='utf8'):
        m=re.match(r'@ (\S+)',l)
        if m: cur=m.group(1); k=0; continue
        m=re.match(r'\s*\*?(\d+) T: (.*)',l)
        if m:
            k=int(m.group(1))-1
            for part in re.sub(r'\s+\[\d+\]\s*$','',m.group(2)).split(' · '):
                if '=' in part:
                    a,g=part.split('=',1); gl.setdefault((cur,k),[]).append((N(a.strip()),g.strip()))
    # E lines in order
    E={}; cur=None
    for l in open(f'eo-align/{ef}.txt',encoding='utf8'):
        if l.startswith('@ '): cur=l[2:].strip(); k=-1; continue
        if l.startswith('= same') or l.startswith('E: '):
            k+=1
            if l.startswith('E: '): E[(cur,k)]=l[3:].strip()
    al=json.load(open(f'eo/{pid}.align.json',encoding='utf8'))
    for cv,cls in al.items():
        if cv.startswith('_'): continue
        for k,cl in enumerate(cls):
            if not cl: continue
            e=E.get((cv,k),''); plain={w.lower().strip("’'") for w in re.findall(r"[A-Za-z’']+",bare(e))}
            g=dict(gl.get((cv,k),[]))
            for a,seg in cl['map']:
                if not seg: continue
                ws=[w.lower().strip("’'") for w in re.findall(r"[A-Za-z’']+",seg)]
                if not ws or not all(w in plain for w in ws): continue   # Onkelos wording (bold) or mixed
                first=a.split()[0]; gg=g.get(first) or g.get(N(first))
                if not gg: continue
                cg=content(gg)
                if not cg or re.search(r'Hashem|^\(?[A-Z]', gg) or re.search(r'\b(Adonoy|Elohim|God)\b', seg): continue
                cs=content(seg)
                if not cs: continue
                if cs & cg: continue
                print(f'{ef} {cv} c{k+1}\t{a}\t= {gg}\t|| {seg}')
