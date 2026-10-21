import re,glob,sys
dry="--dry" in sys.argv
DROP = re.compile(r'''^(Metsudah's|Their)\b.*?(\bfollows? the Hebrew\b.*|\b(is|are) the Hebrew (name|names|word|words|measure)\b.*|\b(is|are) replaced by Onkelos's\b.*|\b(is|are) the same relations?\b.*|\breads the Hebrew differently\b.*)$''')
ORPHAN = {x.lower() for x in {"Their bracket is printed on the next line","This edition of the Targum does not have the matching words, so both drop out",
          '"The voice of" is Metsudah\'s','Onkelos has "to look at it" (לְאִסְתַּכָּלָא בֵהּ) instead'}}
def clean(note):
    note=note.strip()
    toks=re.split(r'((?<=[.;])\s+)', note)   # pieces and separators
    pieces=toks[0::2]; seps=toks[1::2]+['']
    keep=[]; dropped=False
    for p,s in zip(pieces,seps):
        core=p.rstrip('.;').strip()
        if DROP.match(core): dropped=True; continue
        keep.append([p,s])
    if not dropped: return note
    keep=[k for k in keep if k[0].rstrip('.;').strip().lower() not in ORPHAN]
    if not keep: return None
    txt=''.join(p+s for p,s in keep).strip()
    txt=txt.rstrip(';')
    if not txt.endswith('.'): txt+='.'
    if txt[0].islower(): txt=txt[0].upper()+txt[1:]
    return txt
changed=[]; dropped=0
for f in sorted(glob.glob('eo-align/*.txt')):
    out=[]
    for l in open(f).read().split('\n'):
        if l.startswith('! '):
            n=clean(l[2:])
            if n is None: dropped+=1; continue
            if n!=l[2:].strip(): changed.append((f,n))
            out.append('! '+n)
        else: out.append(l)
    if not dry: open(f,'w').write('\n'.join(out))
print('dropped',dropped,'changed',len(changed))
for f,b in changed: print(f.split('/')[-1],'=>',b)
