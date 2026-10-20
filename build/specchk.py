# specchk.py FILE... : list form lines whose spec does not have exactly one stem piece
import re, sys
for f in sys.argv[1:]:
    for ln, l in enumerate(open(f, encoding='utf8'), 1):
        if l.startswith('#') or '|' not in l: continue
        s = re.sub(r'^(~\S+?>)?([a-z]+/)?(\d+:\d+>)?', '', l.split('|')[0].strip())
        ps = re.split(r'\.(?=[֑-ת◌־])', s)
        if sum(1 for p in ps if '=' not in p and '~' not in p) != 1: print(f'{f}:{ln}: {s}')
