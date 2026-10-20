"""Text corrections applied at build time to the finished lines.
FIX[(parsha id, 'c:v')] = {'e': [(old, new), ...], 't': [...], 'h': [...]} : one-off fixes (e.g. from reports on the page)
WORDFIX = [(regex, replacement, expected count across the Chumash)] : clear typos in the Metsudah English"""
import re, collections

FIX = {
    ('chayeisarah', '24:28'): {'e': [('of these these happenings', 'of these happenings')]},  # report 2026-10-20
    ('lechlecha', '14:9'): {'e': [('Sidal, king of Goyim', 'Tidal, king of Goyim')]},        # as in 14:1
}

WORDFIX = [
    (r'\bAngles\b', 'Angels', 1), (r'\bdivid\b', 'divide', 1), (r'\brasied\b', 'raised', 1),
    (r'\btestimonoy\b', 'testimony', 1), (r'\bexept\b', 'except', 1), (r'\byour are\b', 'you are', 2),
    (r'\bthe their land\b', 'their land', 1), (r'\bpromished\b', 'promised', 1), (r'\bseperate\b', 'separate', 1),
    (r'\bthe the midst\b', 'the midst', 1), (r'\bto do perform\b', 'to perform', 1),
    (r'\bwith it it shall\b', 'with it; it shall', 1), (r'\bfor you you shall\b', 'for you; you shall', 1),
    (r'\baccacia\b', 'acacia', 1), (r'\bamd\b', 'and', 1), (r'\bannihalate\b', 'annihilate', 2), (r'\bannoint\b', 'anoint', 1),
    (r'\bannointing\b', 'anointing', 2), (r'\bbeneficience\b', 'beneficence', 1), (r'\bberore\b', 'before', 1),
    (r'\bbretheren\b', 'brethren', 2), (r'\bcomsumed\b', 'consumed', 1), (r'\bconvenant\b', 'covenant', 1),
    (r'\bdistinguised\b', 'distinguished', 1), (r'\beminate\b', 'emanate', 1), (r'\bexcercise\b', 'exercise', 1),
    (r'\bextrememly\b', 'extremely', 1), (r'\bfavorbly\b', 'favorably', 1), (r'\bforified\b', 'fortified', 1),
    (r'\bhemorroids\b', 'hemorrhoids', 1), (r'\binquities\b', 'iniquities', 1), (r'\blibitions\b', 'libations', 1),
    (r'\bmasonary\b', 'masonry', 1), (r'\bmultipying\b', 'multiplying', 1), (r'\bnunbers\b', 'numbers', 1),
    (r'\boppresor\b', 'oppressor', 1), (r'\bpersued\b', 'pursued', 1), (r'\bportentuous\b', 'portentous', 1),
    (r'\bpossesed\b', 'possessed', 1), (r'\bpossesion\b', 'possession', 1), (r'\bprodigous\b', 'prodigious', 1),
    (r'\bsimiliar\b', 'similar', 1), (r'\bsustinance\b', 'sustenance', 1), (r'\bterrritory\b', 'territory', 1),
    (r'\buncleaness\b', 'uncleanness', 1), (r'\bvaulation\b', 'valuation', 1), (r'\bwoud\b', 'would', 1),
    (r'\byeilding\b', 'yielding', 1), (r'\byouselves\b', 'yourselves', 1), (r'\bstubborness\b', 'stubbornness', 2),
    (r'\buncircumcized\b', 'uncircumcised', 1), (r'\bslendor\b', 'splendor', 1), (r'\bopen-sockered\b', 'open-socketed', 1),
    (r'\ba gainst\b', 'against', 1), (r'\bcongrega-tion\b', 'congregation', 1), (r'\bcompen-sation\b', 'compensation', 1),
    (r'\bwomans son\b', 'woman’s son', 1), (r'\bomer waveuplifted-offering\b', 'omer wave-uplifted-offering', 1),
    (r'\bsuch a think\b', 'such a thing', 1),
]
_W = [(re.compile(p), r, n) for p, r, n in WORDFIX]
COUNT = collections.Counter()

def fix_en(s, count=False):
    for k, (rx, r, _) in enumerate(_W):
        s, n = rx.subn(r, s)
        if count: COUNT[k] += n
    return s

def apply(pid, c, v, h, t, e):
    e = [fix_en(x, True) for x in e]
    f = FIX.get((pid, f'{c}:{v}'))
    if not f: return h, t, e
    out = []
    for key, arr in (('h', h), ('t', t), ('e', e)):
        arr = list(arr)
        for old, new in f.get(key, []):
            hits = [k for k, s in enumerate(arr) if old in s]
            if len(hits) != 1: raise SystemExit(f'FIX MISS {pid} {c}:{v} {key} {old!r}')
            arr[hits[0]] = arr[hits[0]].replace(old, new)
        out.append(arr)
    return tuple(out)

def check():
    bad = [(WORDFIX[k][0], COUNT[k], WORDFIX[k][2]) for k in range(len(WORDFIX)) if COUNT[k] != WORDFIX[k][2]]
    if bad: raise SystemExit(f'WORDFIX COUNT {bad}')
    print('wordfix ok', sum(COUNT.values()), 'replacements')
