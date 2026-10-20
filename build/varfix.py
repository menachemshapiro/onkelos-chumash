# varfix.py: split variant-labelled global form entries into a plain global entry + verse-scoped labelled ones
import runpy, sys, re, json, glob, unicodedata as u
N = lambda s: u.normalize('NFC', s)
WRITE = '--write' in sys.argv; sys.argv = ['gloss_build.py', 'todo', 'none']
G = runpy.run_path('gloss_build.py', run_name='bt')
PAR = {}
def inparen(pid):
    if pid not in PAR:
        S = {}
        for r in json.load(open(f'../p/{pid}.json'))['V']:
            t = ' '.join(r['t'])
            for m in re.finditer(r'[(\[]([^)\]]*)[)\]]', t):
                for w in m.group(1).split():
                    S.setdefault(N(re.sub(r'[^א-תְ-ׇ]', '', w)), set()).add(f"{r['c']}:{r['v']}")
        PAR[pid] = S
    return PAR[pid]
def strip(h):
    h = re.sub(r'\s*\((?:a )?variant reading(?:, in brackets)?\)', '', h)
    h = re.sub(r'\s*\(part of a bracketed variant\)', '', h)
    h = h.replace('a variant reading; ', '').replace('; a variant reading', '')
    return h.strip()
# where each global form is used
used = {}
for a in G['ALIYOT']:
    for c, v, toks in a[2]:
        for t in toks: used.setdefault(N(t), set()).add((a[0], f'{c}:{v}'))
for f in sorted(glob.glob('gl/*-*.txt')):
    pid = f.split('/')[-1].rsplit('-', 1)[0]
    L = open(f, encoding='utf8').read().split('\n'); new = []; ch = False
    for line in L:
        p = [x.strip() for x in line.split('|')]
        if line.startswith('#') or re.match(r'^\d+:\d+>', line) or len(p) < 4 or 'variant' not in p[3]:
            new.append(line); continue
        form = N(''.join(re.split(r'[=~]', x)[0] for x in re.split(r'\.(?=[֑-ת◌־])', N(p[0]))).replace('־', '').replace('◌', ''))
        alt = inparen(pid).get(form, set())
        others = {x for x in used.get(form, set()) if not (x[0] == pid and x[1] in alt)}
        h2 = strip(p[3])
        if not others or not h2 or h2 == p[3] or not alt:
            if others: print('CHECK', f, line, sorted(others)[:3], alt)
            new.append(line); continue
        p2 = p[:]; p2[3] = h2; new.append(' | '.join(p2))
        for cv in sorted(alt): new.append(f'{cv}>' + line)
        ch = True; print('FIX', f, form, '->', h2, '| scoped', sorted(alt))
    if ch and '--write' in sys.argv[1:] or (ch and len(__import__('sys').argv) and False): pass
    if ch and WRITE: open(f, 'w', encoding='utf8').write('\n'.join(new))
