"""jas_abbr.py : the two abbreviation lists from the front of Jastrow (2018 Sefaria-Data XML) ->
j/abbr.json {"en": [[abbr, meaning], ...], "he": [[abbr, meaning], ...]}; the pop-up loads it only when its ? button is tapped."""
import re, json, html
SP = '/tmp/claude-0/-home-claude/b2b6b330-0f50-5db3-a7e4-69fa01b487e5/scratchpad/'
X = open(SP + 'jastrow/full/Jastrow-full-2017.xml', encoding='utf8').read()
front = X[:X.index('<body>')]
he_start = front.index('Hebrew or Aramaic Abbreviations'); en_start = front.index('List of Abbreviations.')
def items(block):
    out = []
    for p in re.findall(r'<p>(.*?)</p>', block, re.S):
        p = re.sub(r'<pgbrk[^>]*/>', '', p)
        p = re.sub(r'<italic>(.*?)</italic>', r'<i>\1</i>', p, flags=re.S)
        p = re.sub(r'<sup>(.*?)</sup>', r'<sup>\1</sup>', p, flags=re.S)
        p = re.sub(r'<(?!/?(?:i|sup)>)[^>]+>', '', p)
        p = html.unescape(re.sub(r'\s+', ' ', p)).strip()
        if ' = ' not in p: continue
        a, m = p.split(' = ', 1)
        out.append([a.strip(), m.strip()])
    return out
HE = items(front[he_start:en_start]); EN = items(front[en_start:])
# common in the entries but not in Jastrow's list; shown in the pop-up marked as added here
ADDED = [['Ib.', 'ibidem, in the same place (the book or passage just cited)'], ['m.', 'masculine'], ['f.', 'feminine'], ['fem.', 'feminine'],
    ['h. text', 'Hebrew text (of the Bible verse the Targum translates)'], ['Part.', 'participle'], ['i. e.', 'id est, that is'],
    ['e. g.', 'exempli gratia, for example'], ['sq.', 'sequens, and the following'], ['pass.', 'passive'], ['p.', 'page'],
    ['Pe.', 'Peal'], ['Pa.', 'Pael'], ['Af.', 'Afel'], ['Hof.', 'Hofal'], ['constr.', 'construct state'], ['supra', 'above'], ['infra', 'below'],
    ['Esp.', 'especially'], ['wds.', 'words'], ['quot.', 'quoted'], ['Denom.', 'denominative (formed from a noun)'], ['Chald.', 'Chaldaic (Aramaic)'],
    ['corresp.', 'corresponding'], ['sing.', 'singular'], ['incorr.', 'incorrect, incorrectly'], ['Hebr.', 'Hebrew'], ['Syr.', 'Syriac'],
    ['Arab.', 'Arabic'], ['interch.', 'interchanged, interchangeable'], ['euphem.', 'euphemism, euphemistically'], ['neut.', 'neuter'],
    ['perh.', 'perhaps'], ['Mss.', 'manuscripts'], ['interpret.', 'interpretation'], ['abbr.', 'abbreviation'], ['Dict.', 'Dictionary'],
    ['trnsf.', 'transferred (used figuratively)'], ['sec.', 'second'], ['Bub.', 'Buber’s edition'], ['Amst.', 'Amsterdam edition'],
    ['Krot.', 'Krotoschin edition (of the Y’rushalmi)'], ['Lag.', 'Lagarde’s edition (of the Targumim)'], ['Chr.', 'Chronicles'], ['Ezek.', 'Ezekiel']]
have = {a for a, m in EN}; ADDED = [x for x in ADDED if x[0] not in have]
json.dump({'he': HE, 'en': EN, 'x': ADDED}, open(SP + 'j/abbr.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print(len(HE), 'Hebrew/Aramaic,', len(EN), 'English abbreviations,', len(ADDED), 'added')
