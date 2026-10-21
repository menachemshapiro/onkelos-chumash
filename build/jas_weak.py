"""jas_weak.py : list Jastrow matches that share no meaning word with the glossary, with the other related entries' glosses, for review."""
import json, re, runpy, sys, io, contextlib
with contextlib.redirect_stdout(io.StringIO()): ns = runpy.run_path('jas_match.py')
E, lex, ew, glosses = ns['E'], ns['lex'], ns['ew'], ns['glosses']
M = json.load(open('jas-map.json')); I = json.load(open('../j/index.json'))
def gl(r):
    e = E[r]; d = json.dumps(e.get('content', {}), ensure_ascii=False)
    it = [re.sub(r'<[^>]+>', '', x).strip(' ,.;') for x in re.findall(r'<i>(.*?)</i>', d)]
    it = [x for x in it if len(x) > 2][:3]
    if not it: it = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', d))[:60]]
    r2 = ns['HWMAP'].get(e.get('prev_hw'))
    if 'same' in re.sub(r'<[^>]+>', '', (e.get('language_reference') or '') + d[:300]) and r2 and r2 != r:
        return 'same as ' + E[r2]['headword'] + ' = ' + gl(r2)[:60]
    return '; '.join(it)[:90]
out = []
for k, m in sorted(M.items()):
    v = lex[k]
    if glosses(E[m['rid']]) & ew(v.get('g')): continue
    others = [r for r in (I.get(k, [None, None, [], []])[3] or []) + m['also'] if r != m['rid']]
    out.append(f"{k}\t{v['h']} ({v.get('p','')}): {v.get('g','')[:50]}\n    ✓ {m['rid']} {E[m['rid']]['headword']} [{m['kind']}]: {gl(m['rid'])}" +
               ''.join(f"\n      {r} {E[r]['headword']}: {gl(r)}" for r in dict.fromkeys(others)))
print(len(out), file=sys.stderr)
print('\n'.join(out))
