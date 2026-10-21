"""tg_hl.py : Targum highlights from the word-by-word match, for chapters whose source text has no marks.
A Targum word is highlighted when the English used for it (in the Onkelos English) is all in bold, i.e. Onkelos's own wording."""
import re, unicodedata as u
N = lambda s: u.normalize('NFC', s)
CHAPTERS = {('vayechi', 49), ('behar', 25), ('behar', 26), ('bechukotai', 26), ('bechukotai', 27)}
def words(s): return [w.lower().strip("’'") for w in re.findall(r"[A-Za-z’']+", s)]
def bold_words(e):
    from collections import Counter
    return Counter(w for b in re.findall(r'<b>(.*?)</b>', e) for w in words(b))
def plain_words(e):
    from collections import Counter
    return Counter(words(re.sub(r'\{[^}]*\}', ' ', re.sub(r'<b>.*?</b>', ' ', e))))
STOP = set('the a an of to and in on at by for from with is are was were be his her their its my your our'.split())
def marks(e, amap):
    """one True/False per Aramaic token: True when its English has a bold content word that is not also Metsudah's
    (checked against the source marks elsewhere in the Torah: about 92% precision and 91% recall)"""
    bw, pw = bold_words(e), plain_words(e)
    out = []
    for a, seg in amap:
        ws = words(seg); cw = [w for w in ws if w not in STOP] or ws
        out += [any(bw[w] > 0 and pw[w] == 0 for w in cw)] * len(a.split())
    return out
TOK = re.compile(r'\(|\)|<[^>]+>|[^\s־()<]+')
def apply(t, flags):
    """wrap runs of flagged Targum words in <b>…</b>; words in parentheses are skipped (as in aram_tokens)"""
    t = re.sub(r'</?b>', '', t)
    spans, depth, k = [], 0, 0
    for m in TOK.finditer(t):
        s = m.group(0)
        if s == '(': depth += 1; continue
        if s == ')': depth -= 1; continue
        if s.startswith('<') or depth or not re.search('[א-ת]', s): continue
        if k < len(flags) and flags[k]: spans.append([m.start(), m.end()])
        k += 1
    if k != len(flags): return None
    runs = []
    for a, b in spans:   # join neighbours separated only by space or maqaf
        if runs and re.fullmatch(r'[\s־]*', t[runs[-1][1]:a]): runs[-1][1] = b
        else: runs.append([a, b])
    for a, b in reversed(runs):
        word = t[a:b]; tail = re.search(r'[:.,;]+$', word)
        b2 = b - (len(tail.group(0)) if tail else 0)
        t = t[:a] + '<b>' + t[a:b2] + '</b>' + t[b2:]
    return t
