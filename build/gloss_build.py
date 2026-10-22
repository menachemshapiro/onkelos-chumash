"""Targum Onkelos glossary builder — all aliyos done so far.

Sources
  gloss_bereishit.py   first aliyah of Bereishit (LEX, FORMS), written in the original long format
  gl/lex.txt           more dictionary words:   key | root | headword | part of speech | meaning
  gl/<pid>-<n>.txt     forms for one aliyah:    form | lex key | code | meaning here | note
                       (a line may start with  c:v>  to apply to that pasuk only, for words that mean
                        different things in different places)

Form pieces: the form is written with '.' between its pieces, e.g.  וּ=.לְ=.מִ~inf.ימְנֵי
  text=meaning   an attached word (and, to, his …); an empty meaning on ו ד ל ב כ מ is filled in
  text~meaning   a grammatical marker; meanings may be short keys from MARK below
  bare text      the stem (exactly one piece)
Code: short words expanded by CODE below, e.g. "G pf 3ms" -> "verb, Pe‘al, past, 3rd masc. sing."
      "name" = a proper name (meaning = the English name)

Words not written out are derived when they are a known word plus ו ד ל ב כ מ in front.
Writes ../g/<parsha>.json for each parsha with glossary pesukim, gl-stats.json, and the
GLOSS_RANGES line of the page.
"""
import json, os, re, sys, unicodedata
from collections import OrderedDict
sys.path.insert(0, os.path.dirname(__file__))
import gloss_bereishit as G1

HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(HERE) + '/'
N = lambda s: unicodedata.normalize('NFD', s)
VOW = re.compile(r'[֑-ׇ]')

# ---------- codes ----------
CODE = {
 'v': 'verb', 'n': 'noun', 'a': 'adjective', 'prep': 'preposition', 'conj': 'conjunction', 'adv': 'adverb',
 'part': 'particle', 'pron': 'pronoun', 'num': 'number', 'ord': 'ordinal number', 'interj': 'interjection', 'neg': 'negative',
 'G': 'Pe‘al', 'D': 'Pa‘el', 'C': 'Af‘el', 'Gt': 'Itpe‘el', 'Dt': 'Itpa‘al', 'Ct': 'Ittaf‘al', 'Gp': 'Pe‘il (passive)',
 'Q': '4-letter root', 'Po': 'Po‘el', 'Qt': 'passive of a 4-letter root', 'Sh': 'Shaf‘el', 'Sht': 'Ishtaf‘al',
 'pf': 'past', 'impf': 'imperfect (future)', 'impv': 'imperative', 'ptc': 'participle', 'pp': 'passive participle', 'inf': 'infinitive',
 '3ms': '3rd masc. sing.', '3fs': '3rd fem. sing.', '2ms': '2nd masc. sing.', '2fs': '2nd fem. sing.', '1cs': '1st person sing.',
 '3mp': '3rd masc. pl.', '3fp': '3rd fem. pl.', '2mp': '2nd masc. pl.', '2fp': '2nd fem. pl.', '1cp': '1st person pl.',
 'ms': 'masc. sing.', 'fs': 'fem. sing.', 'mp': 'masc. pl.', 'fp': 'fem. pl.', 'm': 'masc.', 'f': 'fem.', 'sg': 'sing.', 'pl': 'pl.',
 'abs': 'absolute', 'cs': 'construct', 'emph': 'emphatic', 'du': 'dual',
}
PGN_SHORT = {'3ms': 'he', '3fs': 'she', '2ms': 'you', '2fs': 'you (fem.)', '1cs': 'I', '3mp': 'they', '3fp': 'they (fem.)',
             '2mp': 'you (pl.)', '2fp': 'you (fem. pl.)', '1cp': 'we'}
T_SHORT = {'pf': 'past', 'impf': 'future', 'impv': 'command'}
SUFX = lambda p: 'pronoun suffix, ' + CODE.get(p, p)

def expand(code):
    """'G pf 3ms+3ms' -> 'verb, Pe‘al, past, 3rd masc. sing. + pronoun suffix, 3rd masc. sing.'"""
    if code.startswith('!'): return code[1:]
    if code == 'name': return 'proper name (as in the Hebrew)'
    main, *sfx = code.split('+')
    w = main.split()
    out = []
    if w and w[0] in ('G', 'D', 'C', 'Gt', 'Dt', 'Ct', 'Gp', 'Q', 'Qt', 'Sh', 'Sht', 'Po'): out.append('verb')
    out += [CODE.get(x, x.replace('_', ' ')) for x in w]
    s = ', '.join(out)
    for p in sfx: s += ' + ' + SUFX(p)
    return s

def auto_note(code):
    w = code.split('+')[0].split()
    if not w or w[0] not in ('G', 'D', 'C', 'Gt', 'Dt', 'Ct', 'Gp', 'Q', 'Qt', 'Sh', 'Sht', 'Po') or len(w) < 2: return ''
    t = w[1]; pgn = w[2] if len(w) > 2 else ''
    if t in T_SHORT and pgn in PGN_SHORT: return PGN_SHORT[pgn] + ', ' + T_SHORT[t]
    if t in ('ptc', 'pp'): return ('passive participle' if t == 'pp' else 'participle (‑ing)') + (', ' + CODE[pgn] if pgn in CODE else '')
    if t == 'inf': return 'infinitive'
    return ''

MARK = {  # short keys for grammar markers
 'he_f': 'he/it, future', 'she_f': 'she/it, future (or: you)', 'you_f': 'you, future', 'I_f': 'I, future', 'we_f': 'we, future',
 'they_f': 'they, future', 'ypl_f': 'you (pl.), future',
 'she_p': 'she, past', 'they_p': 'they, past', 'you_p': 'you, past', 'I_p': 'I, past', 'we_p': 'we, past', 'ypl_p': 'you (pl.), past',
 'cmd': 'command', 'cs_pl': 'plural, construct (“the … of”)', 'cmd_pl': 'you (pl.), command', 'cmd_fp': 'you (fem. pl.), command', 'cmd_fs': 'you (fem.), command',
 'inf': 'infinitive', 'inf_end': 'infinitive ending', 'ptc': 'participle', 'mp': 'masc. pl.', 'fs': 'fem. sing.', 'fp': 'fem. pl.',
 'C': 'causative (Af‘el)', 'Gt': 'passive (Itpe‘el)', 'Dt': 'passive (Itpa‘al)', 'Ct': 'passive causative (Ittaf‘al)',
 'Sh': 'causative (Shaf‘el)', 'emph': 'emphatic state ≈ “the”', 'emphp': 'emphatic plural ≈ “the”', 'pl': 'plural (absolute)',
 'ptcD': 'participle (Pa‘el)', 'ptcC': 'participle (Af‘el)', 'ptcGt': 'participle (passive)', 'cs_pl': 'plural, construct (“the … of”)',
}
PROCLITIC = {'ו': 'and', 'ד': 'that, which / of', 'ל': 'to, for', 'ב': 'in', 'כ': 'like, as', 'מ': 'from (מִן)'}
HERE_WORD = {'ו': 'and', 'ל': 'to', 'ב': 'in', 'כ': 'like', 'מ': 'from'}

def pieces(spec):
    """'וּ=.לְ=.מִ~inf.ימְנֵי' -> (pre, stem, suf) in page format [[text, meaning, kind]]"""
    ps = re.split(r'\.(?=[\u0591-\u05ea◌־])', spec)
    stems = [i for i, p in enumerate(ps) if '=' not in p and '~' not in p]
    if len(stems) != 1: raise ValueError('need exactly one stem piece: ' + spec)
    si = stems[0]
    def one(p):
        kind = 'g' if '~' in p and ('=' not in p or p.index('~') < p.index('=')) else 'w'
        txt, m = p.split('~' if kind == 'g' else '=', 1)
        if not m and kind == 'w': m = PROCLITIC.get(VOW.sub('', txt)[:1], '')
        m = MARK.get(m, m)
        if txt.startswith('־') and len(txt) > 1 and '֑' <= txt[1] <= 'ׇ': txt = '◌' + txt[1:]
        elif len(txt) and '֑' <= txt[0] <= 'ׇ': txt = '◌' + txt
        return [txt, m, kind]
    return [one(p) for p in ps[:si]], ps[si], [one(p) for p in ps[si + 1:]]

# ---------- dictionary ----------
LEX = {k: dict(zip(['r', 'h', 'p', 'g'], v)) for k, v in G1.LEX.items()}
LEX['name'] = {'r': '', 'h': '', 'p': 'proper name', 'g': 'a name, kept as in the Hebrew'}
def read_lex(path):
    for ln, line in enumerate(open(path, encoding='utf8'), 1):
        line = line.split('#', 1)[0].strip() if not line.lstrip().startswith('#') else ''
        if not line: continue
        f = [x.strip() for x in line.split('|')]
        if len(f) != 5: raise SystemExit(f'{path}:{ln}: need 5 fields: {line}')
        if f[0] in LEX and LEX[f[0]] != dict(zip('rhpg', f[1:])): DUP.append(f'{path}:{ln}: {f[0]} defined twice'); continue
        LEX[f[0]] = dict(zip('rhpg', f[1:]))
DUP = []
if os.path.exists(HERE + '/gl/lex.txt'): read_lex(HERE + '/gl/lex.txt')
if DUP: raise SystemExit('\n'.join(DUP))

# ---------- forms ----------
FORMS = {}       # NFD form -> entry
AT = {}          # 'c:v' -> {NFD form -> entry}
SRC = {}         # NFD form -> which file wrote it
for k, v in G1.FORMS.items():
    e = {'l': v[0], 'pre': G1.parts(v[1]), 'stem': v[2], 'suf': G1.parts(v[3]), 'f': v[4], 'here': v[5]}
    if len(v) > 6 and v[6]: e['sn'] = v[6]
    FORMS[N(k)] = e; SRC[N(k)] = 'b1'

AFTER = {}   # form -> [(previous word ending, entry)]
def read_forms(path, tag):
    for ln, line in enumerate(open(path, encoding='utf8'), 1):
        s = line.strip()
        if not s or s.startswith('#'): continue
        at = None; book = None; after = None
        m = re.match(r'^~(\S+?)>\s*', s)   # ~WORD> : only right after a word ending in WORD (a fixed phrase: מַשְׁכַּן זִמְנָא)
        if m: after, s = N(m.group(1)), s[m.end():]
        m = re.match(r'^(?:([a-z]+)/)?(\d+:\d+)>\s*', s)   # c:v> scopes to this file's book; pid/c:v> to that parsha's book
        if m: book, at, s = m.group(1), m.group(2), s[m.end():]
        f = [x.strip() for x in s.split('|')]
        if len(f) < 4: raise SystemExit(f'{path}:{ln}: need form | lex | code | here [| note]: {line}')
        spec, lex, code, here = f[:4]; note = f[4] if len(f) > 4 else ''
        if lex not in LEX: raise SystemExit(f'{path}:{ln}: unknown dictionary word {lex!r}')
        try: pre, stem, suf = pieces(N(spec))
        except ValueError as e: raise SystemExit(f'{path}:{ln}: {e}')
        form = N(''.join(re.split(r'[=~]', x)[0] for x in re.split(r'\.(?=[\u0591-\u05ea◌־])', spec)).replace('־', '').replace('◌', ''))
        e = {'l': lex, 'pre': pre, 'stem': stem, 'suf': suf, 'f': expand(code), 'here': here}
        sn = note or ('' if any(x[2] == 'g' for x in pre + suf) else auto_note(code))
        if sn: e['sn'] = sn
        if code == 'name': e['name'] = 1
        if after: AFTER.setdefault(form, []).append((after, e)); continue
        if at: AT.setdefault(f'{BOOK[book or tag.rsplit("-", 1)[0]]}|{at}', {})[form] = e
        else:
            if form in FORMS and SRC[form] != tag: pass  # a later aliyah may refine an earlier entry
            FORMS[form] = e; SRC[form] = tag

ALIYOT = json.load(open(HERE + '/gl-aliyot.json', encoding='utf8'))   # [pid, aliyah name, [[c, v, [tokens]]]]
NUM = {'ראשון': 1, 'שני': 2, 'שלישי': 3, 'רביעי': 4, 'חמישי': 5, 'שישי': 6, 'שביעי': 7, 'מפטיר': 8, 'שביעי ומפטיר': 7}
def akey(a): return f'{a[0]}-{NUM[a[1]]}'
BOOK, _b, _last = {}, 0, None   # pid -> book number (a new book starts when the chapter goes back down)
for a in ALIYOT:
    if a[0] not in BOOK:
        if _last and a[2][0][0] < _last: _b += 1
        BOOK[a[0]] = _b
    _last = a[2][-1][0]
for a in ALIYOT:
    p = f'{HERE}/gl/{akey(a)}.txt'
    if os.path.exists(p): read_forms(p, akey(a))
if os.path.exists(f'{HERE}/gl/cleanup.txt'): read_forms(f'{HERE}/gl/cleanup.txt', 'cleanup-1')   # whole-Torah corrections, read last

# ---------- derive ו ד ל ב כ מ + known word ----------
def skel(w):
    """letters and vowels, without dagesh, with the first letter's vowel dropped (it changes after a prefix)"""
    w = N(w).replace('ּ', '').replace('ֿ', '')
    m = re.match(r'([א-ת])([֑-ׇ]*)(.*)', w)
    if not m: return w
    rest = m.group(3)
    first = m.group(1) + ''.join(c for c in m.group(2) if c in 'ׁׂ')   # keep shin/sin dot
    return first + rest
nodag = lambda w: N(w).replace('\u05bc', '')
NODAG = {}
for f in FORMS: NODAG.setdefault(nodag(f), f)
SKEL = {}
for f, e in FORMS.items(): SKEL.setdefault(skel(f), f)
V_ = '[\u0591-\u05c7]*'
PRE_RE = re.compile(f'^(ו{V_})?([דמ]{V_})?([לבכ]{V_})?')   # and · that/from · to/in/like
NO_DERIVE = {'yat', 'al', 'be', 'le', 'min', 'ha', 'had', 'ka'}
CTX_NOTE = re.compile(r'\s*\((?:Hebrew:[^()]*|[^()]*[\u05d0-\u05ea][^()]*=[^()]*|\d+:\d+\)[^;()]*)\)?|;\s*\(\d+:\d+\)[^;]*')
def derive(tok):
    """a known word with ו ד מ ל ב כ in front; returns (entry, base form) or (None, None)"""
    m = PRE_RE.match(tok)
    groups = [g for g in m.groups() if g]
    # try the longest prefix first, then shorter ones
    for n in range(len(groups), 0, -1):
        pre = groups[:n]; rest = tok[len(''.join(pre)):]
        if len(VOW.sub('', rest)) < 2 or rest[0] == 'ו': continue
        if sum(1 for p in pre if VOW.sub('', p) != 'ו') > 1 and len(VOW.sub('', rest)) <= 2: continue   # e.g. מִ+לְ on a 2-letter word: too risky
        short = len(VOW.sub('', rest)) <= 2   # short words must match exactly (apart from a dagesh)
        base = rest if rest in FORMS else NODAG.get(nodag(rest)) if short else SKEL.get(skel(rest))
        if not base or FORMS[base]['l'] in NO_DERIVE: continue
        b = FORMS[base]
        Ls = [VOW.sub('', p) for p in pre]
        if b['f'].startswith('verb') and any(x in 'לבכמ' for x in Ls) and not any(w in b['f'] for w in ('participle', 'infinitive')):
            continue   # a preposition on a finite verb: the letter is part of the word, not a prefix
        nounlike = b['f'].startswith(('noun', 'proper name', 'the Divine')) or b['f'] == 'proper name (as in the Hebrew)'
        words = []; h_override = None
        for p in pre:
            L = VOW.sub('', p)
            if L == 'ד':
                if nounlike: words.append('of')
                elif b['f'].startswith('adjective') or 'participle' in b['f']:
                    h0 = b['here']; be = 'that (are)' if re.search(r'\bpl\.', b['f']) else 'that (is)'
                    lit = re.search(r'\(lit\. (\w+ing\b[^)]*)\)', h0)
                    first = h0.split(' ', 1)[0].strip(',;')
                    if re.match(r'^(is|are|was|were|has|have|had|will|shall|who|which|that)\b', h0): words.append('that')
                    elif b['f'].startswith('adjective') or first.endswith('ing') or ('passive' in b['f'] and not re.match(r'^(is|are|was|were|has|have|had|will|shall)\b', h0)) or first in ('appointed', 'written', 'fit', 'holy', 'clean', 'impure', 'near', 'abhorrent', 'evil', 'proper'):
                        words.append(be)
                    elif lit:
                        words.append(be); h_override = lit.group(1)
                    else: words.append('that')
                else: words.append('that')
            else: words.append(HERE_WORD[L])
        e = dict(b); e['pre'] = [[p, PROCLITIC[VOW.sub('', p)], 'w'] for p in pre] + b['pre']
        h = h_override or b['here']
        while words and h.split(' ', 1)[0] == words[-1]: words.pop()   # no 'of of'
        e['here'] = ' '.join(words + [h])
        e['derived'] = base
        return e, base
    return None, None

# ---------- coverage, stats, output ----------
# ---------- notes that belong to one verse ----------
# A shared gloss may carry a note written for the verse where it was first glossed: an idiom
# "(עַד לָא = not yet)", the Hebrew it renders "(Hebrew: אָסוֹן)", or "; (44:16) has found".
# Such a note is shown only where the verse actually has those words (or is that verse).
_VT = {}
def _cons(x): return re.sub(r'[^א-ת ]', '', N(x).replace('־', ' ').replace('/', ' ')).replace('ך','כ').replace('ם','מ').replace('ן','נ').replace('ף','פ').replace('ץ','צ')
def verse_text(pid, c, v):
    if pid not in _VT:
        _VT[pid] = {}
        try:
            for x in json.load(open(SP + f'p/{pid}.json', encoding='utf8'))['V']:
                h = ' '.join(x['h']) if isinstance(x['h'], list) else str(x['h'])
                t = ' '.join(x['t']) if isinstance(x['t'], list) else str(x['t'])
                en = ' '.join(x.get('e', [])) if isinstance(x.get('e'), list) else str(x.get('e', ''))
                _VT[pid][f"{x['c']}:{x['v']}"] = (' ' + _cons(re.sub(r'<[^>]+>', '', h)) + ' ', ' ' + _cons(re.sub(r'<[^>]+>', '', t)) + ' ', {_skel(w) for w in re.findall(r"[A-Za-z]+", re.sub(r'<[^>]+>', '', en))})
        except FileNotFoundError: pass
    return _VT[pid].get(f'{c}:{v}', (' ', ' ', set()))
def _has(text, words):
    ws = [w for w in _cons(words).split() if w]
    def ok(w):
        cands = [w]
        while len(cands[-1]) > 3 and cands[-1][0] in 'הובלמכש': cands.append(cands[-1][1:])
        return any(x in text for x in cands)
    return bool(ws) and all(ok(w) for w in ws)
NOTE_RE = re.compile(r'\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)')
def fit_notes(here, pid, c, v):
    if '(' not in here and ';' not in here: return here
    heb, aram, _en = verse_text(pid, c, v)
    # "main; (44:16) other": keep the clause only in its verse
    parts = here.split('; ')
    keep = [parts[0]]
    for q in parts[1:]:
        m = re.match(r'\((\d+):(\d+)\)\s*(.*)', q)
        if m:
            if (m.group(1), m.group(2)) == (str(c), str(v)): keep = [m.group(3)]
            continue
        keep.append(q)
    here = '; '.join(keep)
    def one(m):
        body = m.group(1)
        mh = re.match(r'(?:Hebrew|Onkelos):\s*([^,;=]*)', body)
        if mh and re.search('[א-ת]', mh.group(1)):
            src = heb if body.startswith('Hebrew') else aram
            return m.group(0) if _has(src, mh.group(1)) else ''
        mi = re.match(r'([^=]*[א-ת][^=]*)=', body)
        if mi:
            ph = ' '.join(_cons(mi.group(1).replace('…', ' ')).split())
            if ' ' not in ph: return m.group(0) if _has(aram, ph) else ''
            first, rest = ph.split(' ', 1)
            alts = [first]
            while len(alts[-1]) > 2 and alts[-1][0] in 'ובלמכד': alts.append(alts[-1][1:])
            return m.group(0) if any(f'{a} {rest}' in aram for a in alts) else ''
        return m.group(0)
    return NOTE_RE.sub(one, here).strip()

# A verb gloss may name its subject, "(Hashem) had commanded"; the name stays only where the
# verse's English has it (spelling differences aside: Yosef/Yoseif, Paroh/Pharaoh).
def _skel(w):
    w = w.lower().replace('ph', 'p').replace('ch', 'kh')
    return re.sub(r'[aeiouy\'’]', '', w)
NAME_OK = {'I', 'He', 'His', 'Him', 'Me', 'My', 'You', 'Your', 'Who', 'Hebrew', 'Onkelos', 'God', 'Divine', 'Presence', 'Word', 'Memra', 'Torah', 'Sabbath', 'Holy', 'Tabernacle', 'Mishkan', 'Ark'}
HASHEM = {_skel(w) for w in ('Adonoy', 'God', 'Lord', 'Hashem', 'HaShem', 'Elohim', 'Almighty')}
def fit_subject(here, pid, c, v):
    en = verse_text(pid, c, v)[2]
    if not en: return here
    def one(m):
        b = m.group(1)
        if b.startswith(('lit.', 'Hebrew', '=', 'as in', 'i.e.')): return m.group(0)
        names = [w for w in re.findall(r"\b[A-Z][A-Za-z‘’']+", b) if w.split("'")[0].split('’')[0] not in NAME_OK]
        if not names: return m.group(0)
        for w in names:
            w = re.split(r"['’]", w)[0]
            if w == 'Hashem':
                if not (HASHEM & en): return ''
            elif _skel(w) not in en: return ''
        return m.group(0)
    out = re.sub(r'\s*\(([^()]*)\)', one, here).strip()
    return out or here

def lookup(tok, c, v, pid, prev=None):
    k = f'{BOOK[pid]}|{c}:{v}'
    if tok in AT.get(k, {}): return AT[k][tok], 'at'
    if prev and tok in AFTER:
        pn = nodag(prev)
        for w, e in AFTER[tok]:
            if pn.endswith(nodag(w)): return e, 'at'
    if tok in FORMS: e, how = FORMS[tok], 'form'
    elif nodag(tok) in NODAG: e, how = FORMS[NODAG[nodag(tok)]], 'form'
    else:
        e, b = derive(tok)
        if not e: return None, None
        how = 'derived'
    h = fit_notes(e.get('here', ''), pid, c, v)
    if e.get('f', '').startswith('verb'): h = fit_subject(h, pid, c, v)
    if h != e.get('here', ''): e = dict(e); e['here'] = h
    return e, how

def done(a):
    k = akey(a)
    return k == 'bereishit-1' or os.path.exists(f'{HERE}/gl/{k}.txt')

def root_of(e):
    L = LEX.get(e['l'], {})
    return L.get('r') or ''

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'build'
    if cmd == 'todo':   # list what an aliyah still needs: python3 gloss_build.py todo vayera-3
        want = sys.argv[2]
        a = next(a for a in ALIYOT if akey(a) == want)
        miss = OrderedDict(); der = OrderedDict()
        for c, v, toks in a[2]:
            for i, t in enumerate(toks):
                e, how = lookup(t, c, v, a[0], toks[i - 1] if i else None)
                if not e: miss.setdefault(t, []).append(f'{c}:{v}')
                elif how == 'derived': der.setdefault(t, (e['derived'], e['here'], f'{c}:{v}'))
        print(f'# {want}: {sum(len(t) for _,_,t in a[2])} words; {len(miss)} forms to write; {len(der)} derived')
        for t, (b, h, cv) in der.items(): print(f'~ {t}  <- {b}  "{h}"  {cv}')
        for t, cvs in miss.items(): print(f'? {t}  {" ".join(cvs[:4])}')
        sys.exit()

    # stats in reading order, only for aliyos that are done
    seen_forms, seen_roots, stats, ranges, out = set(), set(), [], {}, {}
    calls = {}
    if os.path.exists(HERE + '/cal-log.json'):
        for c in json.load(open(HERE + '/cal-log.json'))['calls']: calls[c['aliyah']] = calls.get(c['aliyah'], 0) + 1
    problems = []
    for a in ALIYOT:
        if not done(a): break
        k = akey(a); pid = a[0]
        toks = [(c, v, t, ts[i - 1] if i else None) for c, v, ts in a[2] for i, t in enumerate(ts)]
        forms = set(t for _, _, t, _ in toks)
        roots = set()
        for c, v, t, prev in toks:
            e, how = lookup(t, c, v, a[0], prev)
            if not e: problems.append(f'{k} {c}:{v} {t}'); continue
            r = root_of(e)
            if r: roots.add(r)
            dst = out.setdefault(pid, {'forms': {}, 'at': {}, 'lex': {}})
            ee = {x: y for x, y in e.items() if x not in ('derived', 'name')}
            if 'here' in ee and '(He)' in ee['here']: ee['here'] = ee['here'].replace('(He)', '(he)')   # the same spelling serves every speaker
            if how == 'at' or (t in dst['forms'] and dst['forms'][t] != ee): dst['at'].setdefault(f'{c}:{v}', {})[t] = ee
            else: dst['forms'][t] = ee
            dst['lex'][e['l']] = LEX[e['l']]
        stats.append({'aliyah': k, 'parsha': pid, 'name': a[1], 'from': a[2][0][:2], 'to': a[2][-1][:2],
                      'words': len(toks), 'forms': len(forms), 'forms_repeat': len(forms & seen_forms), 'forms_new': len(forms - seen_forms),
                      'roots': len(roots), 'roots_new': len(roots - seen_roots), 'roots_repeat': len(roots & seen_roots),
                      'cal': calls.get(k, 0)})
        seen_forms |= forms; seen_roots |= roots
        ranges.setdefault(pid, []).append([a[2][0][0], a[2][0][1], a[2][-1][0], a[2][-1][1]])
    if problems:
        print('MISSING', len(problems)); print('\n'.join(problems[:40])); sys.exit(1)
    os.makedirs(SP + 'g', exist_ok=True)
    for pid, d in out.items():
        d['ranges'] = ranges[pid]
        json.dump(d, open(SP + f'g/{pid}.json', 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    json.dump(stats, open(HERE + '/gl-stats.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
    # merge consecutive ranges per parsha
    rng = {}
    for pid, rs in ranges.items():
        m = [rs[0][:]]
        for r in rs[1:]:
            m[-1][2:] = r[2:]   # aliyos are consecutive
        rng[pid] = m
    page = SP + 'bereishit-onkelos.html'
    s = open(page, encoding='utf8').read()
    s2 = re.sub(r'const GLOSS_RANGES = .*?;\n', 'const GLOSS_RANGES = ' + json.dumps(rng) + ';\n', s, count=1)
    if s2 != s: open(page, 'w', encoding='utf8').write(s2)
    print(len(stats), 'aliyos ·', len(FORMS), 'forms ·', len(LEX), 'dictionary words ·', 'ranges', rng)
