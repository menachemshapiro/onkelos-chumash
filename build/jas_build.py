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
os.makedirs(SP + 'j', exist_ok=True)
for f in glob.glob(SP + 'j/*.json'): os.remove(f)
idx, groups = {}, collections.defaultdict(dict)
for k, m in M.items():
    idx[k] = [m['rid'], m['kind'], m['also']]
    for r in [m['rid']] + m['also']:
        groups[r[0]][r] = {'h': E[r]['headword'], 'html': render(E[r])}
json.dump(idx, open(SP + 'j/index.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
for g, d in groups.items(): json.dump(d, open(SP + f'j/{g}.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print(len(idx), 'glossary words;', sum(len(d) for d in groups.values()), 'entries in', len(groups), 'files')
