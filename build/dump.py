import json, re, sys, subprocess, os
pid, rng = sys.argv[1], sys.argv[2]; ovr = sys.argv[3] if len(sys.argv) > 3 else None
env = dict(os.environ, RANGE=rng, OUT=f'data-{pid}.json')
r = subprocess.run(['python3', '-I', 'align.py'] + ([ovr] if ovr else []), env=env, capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip()[-2000:])
d = json.load(open(f'data-{pid}.json'))
only = None
if ovr and len(sys.argv) > 4: only = set(json.load(open(ovr)))
N = re.compile(r'[֑-ׇ]')
out = []
for x in d:
    k = f"{x['c']}:{x['v']}"
    if len(x['h']) < 2 or (only is not None and k not in only): continue
    out.append(k)
    for a, b, c in zip(x['h'], x['t'], x['e']):
        out.append(' ' + N.sub('', a) + ' | ' + N.sub('', re.sub('<[^>]+>', '', b)) + ' | ' + re.sub('<[^>]+>', '', c))
open(f'dump-{pid}.txt', 'w').write('\n'.join(out) + '\n')
print(len(d), 'verses;', len(out), 'lines')
