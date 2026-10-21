import json,sys
for pid in sys.argv[1:]:
    a=json.load(open(f'pubcheck/p/{pid}.json')); b=json.load(open(f'p/{pid}.json'))
    s=lambda d:[{k:x for k,x in v.items() if k not in('eo','ea')} for v in d['V']]
    o=[k for k in set(a)|set(b) if k!='V' and a.get(k)!=b.get(k)]
    print(pid, 'ok' if s(a)==s(b) and not o else ('DIFF',o))
