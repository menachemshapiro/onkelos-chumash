"""lit_merge.py : add the exact (literal) English to the Onkelos word-by-word table, from build/lit/<parsha>.txt.

File format:  "@ c:v.clause"  then one line per Aramaic word, or per group of words read together:
    Aramaic | exact English
The groups must cover the clause's Aramaic words in order (the same words as the word-by-word match, v['ea']).
Writes v['el'][clause] = [[Aramaic, exact English, English used in the translation], ...] into p/<parsha>.json.
The page shows the exact English, with the English used in parentheses when it is different.
Run after eo_merge.py (eo_merge.py calls it)."""
import json, os, re, glob, sys, unicodedata as u
HERE = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(HERE) + '/'
N = lambda s: u.normalize('NFC', s)

def read(fn):
    out, cur = {}, None
    for ln in open(fn, encoding='utf8'):
        ln = ln.rstrip('\n')
        if not ln.strip() or ln.startswith('#'): continue
        if ln.startswith('@ '): cur = ln[2:].strip(); out[cur] = []; continue
        a, e = [x.strip() for x in ln.split('|', 1)]
        out[cur].append((N(a), e))
    return out

def merge(verbose=True):
    n = 0
    for pf in sorted(glob.glob(SP + 'p/*.json')):
        pid = os.path.basename(pf)[:-5]; src = HERE + f'/lit/{pid}.txt'
        d = json.load(open(pf, encoding='utf8')); L = read(src) if os.path.exists(src) else {}
        changed = False
        for v in d['V']:
            el = None
            for j, a in enumerate(v.get('ea') or []):
                key = f"{v['c']}:{v['v']}.{j}"
                if key not in L: continue
                if not a: raise SystemExit(f'{pid} {key}: no word-by-word match for this clause')
                words = [N(w) for ar, en in a['map'] for w in ar.split()]
                owner = [k for k, (ar, en) in enumerate(a['map']) for w in ar.split()]
                rows, i = [], 0
                for ar, ex in L[key]:
                    ws = ar.split()
                    if words[i:i + len(ws)] != ws:
                        raise SystemExit(f'{pid} {key}: "{ar}" does not match the next words "{" ".join(words[i:i + len(ws)])}"')
                    used = []
                    for k in dict.fromkeys(owner[i:i + len(ws)]):
                        e = a['map'][k][1]
                        if e and e not in used: used.append(e)
                    rows.append([ar, ex, ' '.join(used)]); i += len(ws)
                if i != len(words): raise SystemExit(f'{pid} {key}: words left over: {" ".join(words[i:])}')
                el = el or [None] * len(v['ea']); el[j] = rows; n += 1
            if el != v.get('el'):
                if el: v['el'] = el
                else: v.pop('el', None)
                changed = True
        if changed: json.dump(d, open(pf, 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    if verbose: print('lit:', n, 'clauses with exact English')

if __name__ == '__main__': merge()
