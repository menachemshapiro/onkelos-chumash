# xcheck.py: list words in earlier books whose entry now comes from a later aliyah's file
# (derived from a later base, or an exact form redefined later) -- these may have changed meaning.
import runpy, sys, unicodedata as u
sys.argv = ['gloss_build.py', 'todo', 'none']
G = runpy.run_path('gloss_build.py', run_name='xcheck')
FORMS, SRC, ALIYOT, lookup, akey = G['FORMS'], G['SRC'], G['ALIYOT'], G['lookup'], G['akey']
order = [akey(a) for a in ALIYOT]; pos = {k: i for i, k in enumerate(order)}
upto = sys.argv[1] if len(sys.argv) > 1 else None
seen = set()
for a in ALIYOT:
    k = akey(a)
    for c, v, toks in a[2]:
        for t in toks:
            e, how = lookup(t, c, v, a[0])
            if not e: continue
            base = e.get('derived', t) if how == 'derived' else t
            src = SRC.get(base) or SRC.get(G['NODAG'].get(G['nodag'](base), ''), '')
            if src in pos and pos[src] > pos[k] and (t, src) not in seen:
                seen.add((t, src)); print(k, f'{c}:{v}', u.normalize('NFC', t), '<-', src, '|', e['here'][:50])
