# booktodo.py pid... : all forms still missing in these parshiyot, with counts and first reference,
# sorted by reading order; writes book-todo.txt
import runpy, sys, unicodedata as u
from collections import OrderedDict
pids = sys.argv[1:]; sys.argv = ['gloss_build.py', 'todo', 'none']
G = runpy.run_path('gloss_build.py', run_name='bt')
miss = OrderedDict(); der = OrderedDict(); words = 0
for a in G['ALIYOT']:
    if a[0] not in pids: continue
    k = G['akey'](a)
    for c, v, toks in a[2]:
        for t in toks:
            words += 1
            e, how = G['lookup'](t, c, v, a[0], toks[i - 1] if i else None)
            if not e: miss.setdefault(t, [k, f'{c}:{v}', 0])[2] += 1
            elif how == 'derived': der.setdefault(t, (k, f'{c}:{v}', e['derived'], e['here']))
with open('book-todo.txt', 'w') as f:
    for t, (k, cv, n) in miss.items(): f.write(f'{u.normalize("NFC", t)}\t{n}\t{k}\t{cv}\n')
with open('book-derived.txt', 'w') as f:
    for t, (k, cv, b, h) in der.items(): f.write(f'{u.normalize("NFC", t)}\t{k}\t{cv}\t{u.normalize("NFC", b)}\t{h}\n')
print(words, 'words;', len(miss), 'forms missing;', len(der), 'derived', sum(x[2] for x in miss.values()), 'tokens missing')
