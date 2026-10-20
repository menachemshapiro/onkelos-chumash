# gdiff.py OLD_DIR NEW_DIR pid... : show glossary entries whose meaning changed
import json, sys, unicodedata as u
old, new = sys.argv[1], sys.argv[2]
for p in sys.argv[3:]:
    a = json.load(open(f'{old}/g/{p}.json')); b = json.load(open(f'{new}/g/{p}.json'))
    def flat(d):
        r = {k: v for k, v in d['forms'].items()}
        for cv, m in d['at'].items():
            for k, v in m.items(): r[f'{cv} {k}'] = v
        return r
    A, B = flat(a), flat(b)
    for k in sorted(set(A) | set(B)):
        x, y = A.get(k), B.get(k)
        hx = x and (x['l'], x['here'], x['f']); hy = y and (y['l'], y['here'], y['f'])
        if hx != hy: print(p, u.normalize('NFC', k), '|', hx and hx[1], '=>', hy and hy[1])
