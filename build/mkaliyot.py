# mkaliyot.py pid... : add these parshiyot to gl-aliyot.json (tokens as the page makes them tappable)
import json, sys, re, unicodedata as u
NAMES = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שביעי', 'מפטיר']
WORD = re.compile(r'[א-ת][֑-ׇא-ת]*')
def toks(t):
    t = re.sub(r'<small>.*?</small>', ' ', t)
    t = re.sub(r'\((?:נ"א|ס"א|לפרש"י)', '( ', t)          # alt-reading labels the page shows in <small>
    t = re.sub(r'<[^>]+>', '', t)
    return [u.normalize('NFD', re.sub('[֑-ֽ֯]', '', w)) for w in WORD.findall(t)]
def build(pid):
    out = []; cur = None
    for v in json.load(open(f'../p/{pid}.json'))['V']:
        if v.get('a'): cur = [pid, v['a'], []]; out.append(cur)
        if cur: cur[2].append([v['c'], v['v'], [w for t in v['t'] for w in toks(t)]])
    return out
if __name__ == '__main__':
    A = json.load(open('gl-aliyot.json'))
    if sys.argv[1] == 'test':
        for pid in sys.argv[2:]:
            old = [a for a in A if a[0] == pid]; new = build(pid)
            d = sum(1 for x, y in zip(old, new) for p, q in zip(x[2], y[2]) if p != q)
            print(pid, len(old), len(new), 'verses differing:', d)
            for x, y in zip(old, new):
                for p, q in zip(x[2], y[2]):
                    if p != q: print('  ', p[0], p[1], [w for w in p[2] if w not in q[2]][:5], [w for w in q[2] if w not in p[2]][:5]); break
        sys.exit()
    have = {a[0] for a in A}
    for pid in sys.argv[1:]:
        if pid not in have: A += build(pid)
    json.dump(A, open('gl-aliyot.json', 'w'), ensure_ascii=False)
    print(len(A), 'aliyot')
