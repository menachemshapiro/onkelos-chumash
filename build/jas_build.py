"""jas_build.py : write the Jastrow pop-up data from jastrow/jastrow-lookups.json and build/jas-map.json.
  j/index.json      {glossary lex id: [rid, "word"|"root", [other rids]]}
  j/<A..Z>.json     {rid: {"h": headword, "html": entry as safe HTML}}, grouped by the first letter of the rid"""
import json, os, re, html, collections, glob
SP = '/tmp/claude-0/-home-claude/b2b6b330-0f50-5db3-a7e4-69fa01b487e5/scratchpad/'
E = json.load(open(SP + 'jastrow/jastrow-lookups.json', encoding='utf8'))['entries']
M = json.load(open(SP + 'build/jas-map.json', encoding='utf8'))
TAG = re.compile(r'<(/?)(\w+)([^>]*)>')
def clean(s):
    """keep <i>, <b>, <sup>, rtl spans and Sefaria reference links; drop every other tag"""
    def fix(m):
        close, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in ('i', 'b', 'sup', 'sub'): return f'<{close}{tag}>'
        if tag == 'span': return '</span>' if close else ('<span dir="rtl">' if 'rtl' in attrs else '<span>')
        if tag == 'a':
            if close: return '</a>'
            h = re.search(r'href="([^"]*)"', attrs)
            if not h: return '<a>'
            href = h.group(1); href = href if href.startswith('/') else '/' + href
            rtl = ' dir="rtl"' if 'rtl' in attrs else ''
            return f'<a{rtl} href="https://www.sefaria.org{html.escape(href, quote=True)}" target="_blank" rel="noopener">'
        return ''
    s = TAG.sub(fix, s or '')
    return re.sub(r'<a>(.*?)</a>', r'\1', s)
def senses(lst):
    out = []
    for s in lst or []:
        if not isinstance(s, dict): continue
        part = ''
        if s.get('number'): part += f'<b class="jn">{html.escape(s["number"])}</b> '
        g = s.get('grammar')
        if g:
            part += f'<b class="jg">{html.escape(g.get("verbal_stem", ""))}</b> ' + ', '.join(f'<span dir="rtl">{html.escape(x)}</span>' for x in g.get('binyan_form', [])) + ' '
        if s.get('definition'): part += clean(s['definition'])
        if s.get('senses'): part += '<div class="jsub">' + senses(s['senses']) + '</div>'
        if part.strip(): out.append(f'<p>{part}</p>')
    return ''.join(out)
def render(e):
    head = ' '.join(x for x in [clean(e.get('language_code', '')), clean(e.get('language_reference', '')), html.escape((e.get('content') or {}).get('morphology', ''))] if x and x.strip())
    body = senses((e.get('content') or {}).get('senses'))
    return (f'<p class="jhead">{head}</p>' if head else '') + body
import unicodedata as u
def base(h): return re.sub(r'\s*([IVX]+|[¹²³⁴⁵])$', '', h.strip().lstrip('*'))
def voc(h): return re.sub(r'[^\u05b0-\u05bc\u05c1\u05c2\u05c7\u05d0-\u05ea]', '', u.normalize('NFD', base(h)))
BYV = collections.defaultdict(list)
for r, e in E.items(): BYV[voc(e['headword'])].append(r)
def key(h, dots=False):
    """letters only, final forms normalised, a weak last letter (א ה י) read as ה: צְלֵי, צְלָא, צָלָה, צָלִי all give צלה.
    With dots=True, shin and sin stay apart (שׁ → ש1, שׂ → ש2)."""
    t = u.normalize('NFD', base(h))
    if dots: t = re.sub(r'ש([\u0591-\u05c7]*?)\u05c1', r'1\1', re.sub(r'ש([\u0591-\u05c7]*?)\u05c2', r'2\1', t))
    c = re.sub(r'[^\u05d0-\u05ea12]', '', t).translate(str.maketrans('ךםןףץ', 'כמנפצ'))
    return c[:-1] + 'ה' if len(c) > 2 and c[-1] in 'אהי' else c
def alts(e): return [a for a in (e.get('alt_headwords') or []) if '׳' not in a and "'" not in a]   # skip abbreviated forms like צִלְ׳
BYK = collections.defaultdict(set)
for r, e in E.items():
    for h in [e['headword']] + alts(e): BYK[key(h)].add(r)
def clash(a, b):
    """True when both forms mark shin/sin and they differ"""
    da, db = re.sub(r'[^12]', '', a), re.sub(r'[^12]', '', b)
    return bool(da and db and da != db)
def related(rid, word):
    """every entry with the same letters as the matched entry or the glossary word (headword or alternative form), in dictionary order"""
    e = E[rid]; forms = [e['headword']] + alts(e) + [word]
    ks = {key(h) for h in forms}; dk = [key(h, True) for h in forms]
    out = set()
    for r in set().union(*(BYK[k] for k in ks)):
        fr = [key(h, True) for h in [E[r]['headword']] + alts(E[r])]
        if any(not clash(a, b) and key_eq(a, b) for a in dk for b in fr): out.add(r)
    return sorted(out | {rid})
def key_eq(a, b): return re.sub(r'[12]', 'ש', a) == re.sub(r'[12]', 'ש', b)
os.makedirs(SP + 'j', exist_ok=True)
for f in glob.glob(SP + 'j/*.json'): os.remove(f)
LEX = {}
for f in glob.glob(SP + 'g/*.json'):
    for k, v in json.load(open(f, encoding='utf8'))['lex'].items(): LEX.setdefault(k, v)
idx, groups = {}, collections.defaultdict(dict)
for k, m in M.items():
    tabs = related(m['rid'], LEX[k]['h'])
    also = [r for r in m['also'] if r not in tabs]
    idx[k] = [m['rid'], m['kind'], also, tabs if len(tabs) > 1 else []]
    for r in [m['rid']] + also + tabs:
        groups[r[0]][r] = {'h': E[r]['headword'], 'a': alts(E[r])[:2], 'html': render(E[r])}
json.dump(idx, open(SP + 'j/index.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
for g, d in groups.items(): json.dump(d, open(SP + f'j/{g}.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print(len(idx), 'glossary words;', sum(len(d) for d in groups.values()), 'entries in', len(groups), 'files')
