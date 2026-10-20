# varleak.py: global form entries labelled "variant" — list every verse they are used in
import runpy, sys, re
sys.argv = ['gloss_build.py', 'todo', 'none']
G = runpy.run_path('gloss_build.py', run_name='bt')
from collections import defaultdict
use = defaultdict(list)
for a in G['ALIYOT']:
    k = G['akey'](a)
    for c, v, toks in a[2]:
        for t in toks:
            e, how = G['lookup'](t, c, v, a[0])
            if e and 'variant' in e.get('here', ''):
                use[(id(e), e['here'])].append((k, f'{c}:{v}', t, how))
for (i, h), L in use.items():
    if len(L) > 1 or L[0][3] == 'derived':
        print(h, '::', ' '.join(f'{a}/{cv}/{t}/{how[0]}' for a, cv, t, how in L))
