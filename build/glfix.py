"""Apply hand-checked glossary fixes (Oct 22 meaning check) to gl/*.txt and gl/lex.txt.

build/glfix.tsv, one fix per line (tab-separated), # for comments:
  F  pid|*  form|*  oldlex  newlex|-  newhere|-  [regex the old 'here' must match]
  A  a full gl line appended to gl/cleanup.txt (pid/c:v>form | lex | code | here)
  L  key | root | headword | part of speech | meaning      (adds or replaces a lex line)
Forms are compared with the piece marks (= ~ .) removed.  Run, then gloss_build.py.
"""
import re, glob, os, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
N = lambda s: unicodedata.normalize('NFC', s)
def joined(form):
    return N(''.join(re.sub(r'[=~].*', '', p) for p in form.split('.')))
fixes, lexes, adds = [], [], []
for ln in open(HERE + '/glfix.tsv', encoding='utf8'):
    ln = ln.rstrip('\n')
    if not ln.strip() or ln.startswith('#'): continue
    f = ln.split('\t')
    if f[0] == 'F':
        f += [''] * (7 - len(f)); fixes.append(f[1:7])
    elif f[0] == 'L': lexes.append(f[1].strip())
    elif f[0] == 'A': adds.append(f[1].strip())
used = [0] * len(fixes)
for fn in sorted(glob.glob(HERE + '/gl/*-*.txt')) + [HERE + '/gl/cleanup.txt']:
    fpid = os.path.basename(fn).rsplit('-', 1)[0]
    lines = open(fn, encoding='utf8').read().split('\n'); ch = False
    for i, ln in enumerate(lines):
        if not ln or ln.startswith('#') or '|' not in ln: continue
        parts = [p.strip() for p in ln.split('|')]
        m = re.match(r'((?:(\w+)/)?(?:\d+:\d+)?>)?(.*)', parts[0]); pre, form = m.group(1) or '', m.group(3)
        pid = m.group(2) or (fpid if fpid != 'cleanup.txt' else '*')
        for j, (fp, ff, old, new, here, rx) in enumerate(fixes):
            if (fp != '*' and pid not in ('*', fp)) or parts[1] != old: continue
            if ff != '*' and joined(form) != N(ff): continue
            if rx and not re.search(rx, parts[3] if len(parts) > 3 else ''): continue
            if new and new != '-': parts[1] = new
            if here and here != '-': parts[3] = here
            used[j] += 1
            lines[i] = ' | '.join([pre + form] + parts[1:]); ch = True
            break
    if ch: open(fn, 'w', encoding='utf8').write('\n'.join(lines))
if adds:
    with open(HERE + '/gl/cleanup.txt', 'a', encoding='utf8') as fh: fh.write('\n# --- Oct 22 meaning check ---\n' + '\n'.join(adds) + '\n')
lp = HERE + '/gl/lex.txt'; L = open(lp, encoding='utf8').read().split('\n')
keys = {l.split('|')[0].strip(): i for i, l in enumerate(L) if '|' in l and not l.startswith('#')}
for x in lexes:
    k = x.split('|')[0].strip()
    if k in keys: L[keys[k]] = x
    else: L.append(x); keys[k] = len(L) - 1
open(lp, 'w', encoding='utf8').write('\n'.join(L))
for j, f in enumerate(fixes):
    if not used[j]: print('UNUSED', f)
print(sum(used), 'form lines changed;', len(lexes), 'lex lines set')
