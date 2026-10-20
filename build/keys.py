# keys.py FILE... : list lex keys used in form files that the dictionary does not have; or `keys.py -h WORD...` to search headwords/meanings
import sys, re, runpy, unicodedata as u
sys.argv, args = ['gloss_build.py', 'todo', 'none'], sys.argv[1:]
import io, contextlib
src = open('gloss_build.py', encoding='utf8').read().split('\nALIYOT = ')[0]
G = {'__name__': 'bt', '__file__': __import__('os').path.abspath('gloss_build.py')}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, 'gloss_build.py', 'exec'), G)
L = G['LEX']
if args and args[0] == '-h':
    V = lambda s: re.sub(r'[֑-ׇ]', '', u.normalize('NFD', s))
    for w in args[1:]:
        print(w, '->', '; '.join(f"{k}={v['h']}({v['g'][:40]})" for k, v in L.items() if V(w) == V(v['h']) or w.lower() in v['g'].lower())[:400])
    sys.exit()
for f in args:
    for ln, line in enumerate(open(f, encoding='utf8'), 1):
        if line.startswith('#') or '|' not in line: continue
        k = line.split('|')[1].strip()
        if k not in L: print(f'{f}:{ln}: {k}')
