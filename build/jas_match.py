"""jas_match.py : match each glossary dictionary entry (lex) to its Jastrow entry from jastrow/jastrow-lookups.json.
Writes build/jas-map.json {lex_id: [best_rid, ...others]} and prints a summary."""
import json, glob, re, collections, unicodedata as u
SP = '/tmp/claude-0/-home-claude/b2b6b330-0f50-5db3-a7e4-69fa01b487e5/scratchpad/'
J = json.load(open(SP + 'jastrow/jastrow-lookups.json', encoding='utf8')); Q, E = J['queries'], J['entries']
lex = {}
for f in glob.glob(SP + 'g/*.json'):
    for k, v in json.load(open(f, encoding='utf8'))['lex'].items(): lex.setdefault(k, v)
def cons(s):
    s = u.normalize('NFD', s or ''); s = re.sub(r'[^א-ת]', '', s)
    return s.translate(str.maketrans('ךםןףץ', 'כמנפצ'))
def voc(s): return re.sub(r'[^ְ-ׇּׁׂא-ת]', '', u.normalize('NFD', s or ''))
def hw(e): return re.sub(r'\s+[IVX]+$|^\*', '', e['headword'].strip())
STOP = set('the a an of to and in or be is as for by on at with from that this it his her its'.split())
def ew(s): return {w for w in re.findall(r'[a-z]+', (s or '').lower()) if w not in STOP and len(w) > 2}
BYC = collections.defaultdict(list)
for rid, e in E.items(): BYC[cons(hw(e))].append(rid)
BYV = collections.defaultdict(list)
for rid, e in E.items(): BYV[voc(hw(e))].append(rid)
def text(e): return re.sub(r'<[^>]+>', '', json.dumps(e.get('content', {}), ensure_ascii=False))
def resolve(rid, depth=0):
    """follow a bare cross-reference ("v. X", "= X") to the entry it points to, when we have it"""
    e = E[rid]; t = text(e)
    defs = ' '.join(s_.get('definition', '') for s_ in e.get('content', {}).get('senses', []) if isinstance(s_, dict))
    plain = re.sub(r'<[^>]+>', '', defs).strip(' ,.;')
    m = re.match(r'^(?:same,?\s*)?(?:v\.|=)\s*(?:sub\s+)?([\u0590-\u05ff*]+(?:\s+[IVX]+)?)', plain)
    if depth < 2 and m and len(plain) < 45:
        tgt = m.group(1).strip('*')
        for r in BYV.get(voc(re.sub(r'\s+[IVX]+$', '', tgt)), []) + BYC.get(cons(tgt), []):
            if r != rid and hw(E[r]) == re.sub(r'\s+[IVX]+$', '', tgt) or (r != rid and cons(hw(E[r])) == cons(tgt)):
                return resolve(r, depth + 1)
    return rid
def verbal(e):
    d = json.dumps(e.get('content', {}), ensure_ascii=False)
    return bool(re.search(r'<i>\s*to |binyan|"Pa\.|Pa\. |Af\. |Ithpa', d[:1500]))
def glosses(e):
    d = json.dumps(e.get('content', {}), ensure_ascii=False) + (e.get('language_reference') or '')
    return ew(' '.join(re.findall(r'<i>(.*?)</i>', d)) + ' ' + ' '.join(re.findall(r'[a-z][a-z ,;-]{2,40}', text(e)[:200])))
def score(v, rid):
    e = E[rid]; h = hw(e); sc = 0; kind = 'word'; vx = False
    if cons(h) == cons(v['h']): vx = voc(h) == voc(v['h']); sc += 10 + (3 if vx else 0)
    elif any(cons(a) == cons(v['h']) for a in e.get('alt_headwords', [])): sc += 8; vx = any(voc(a) == voc(v['h']) for a in e.get('alt_headwords', []))
    elif v.get('r') and cons(h) == cons(v['r']): kind = 'root'; sc += 4
    else: return (-1, kind, rid)
    tgt = resolve(rid); t = E[tgt]
    ov = len(glosses(t) & ew(v.get('g')))
    if kind == 'root' and not (((v.get('p') or '').startswith('verb') and verbal(t)) or ov): return (-1, kind, tgt)
    if kind == 'word' and not (vx or ov): return (-1, kind, tgt)
    isverb = (v.get('p') or '').startswith('verb')
    if kind == 'word': sc += 2 if isverb == verbal(t) else -2
    d = json.dumps(t.get('content', {}), ensure_ascii=False)
    if 'ch' in (t.get('language_code') or ''): sc += 1
    if 'Onkelos' in d: sc += 2
    elif 'Targ' in d: sc += 1
    sc += min(8, 2 * ov)
    return (sc, kind, tgt)
out, stat = {}, collections.Counter()
for k, v in lex.items():
    if not v.get('h') or v.get('p') in ('the Divine Name',): continue
    cands = set(Q.get(v['h'], [])) | set(BYC.get(cons(v['h']), [])) | (set(BYC.get(cons(v['r']), [])) if v.get('r') else set())
    sc = sorted((score(v, r) for r in cands), key=lambda x: -x[0])
    sc = [x for x in sc if x[0] >= 6]
    seen = []
    for x in sc:
        if x[2] not in seen: seen.append(x[2])
    if sc: out[k] = {'rid': sc[0][2], 'kind': sc[0][1], 'also': seen[1:3]}; stat[sc[0][1]] += 1
    else: stat['none'] += 1
json.dump(out, open(SP + 'build/jas-map.json', 'w', encoding='utf8'), ensure_ascii=False)
print(stat)
