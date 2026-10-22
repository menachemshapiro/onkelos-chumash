"""jas_fix.py : hand fixes to Sefaria's Jastrow data, checked against scans of the 1903 printing
(from Menachem's other project, "Jastrow (Sefaria data): damaged binyan labels and entries", Oct 23, 2026).
Applied by jas_build.py to the downloaded entries every time it runs; the downloaded files are left as they are.

  STEM     a binyan whose name was lost (only "*." or "[." survived): the name from the scan
  SPLIT    a separate entry stuck onto the end of the entry before it as a fake binyan: made its own entry
           (id = host id + "b"), shown right after the host entry
  O01711   "נִסְתַּר." put in the binyan-name slot: the name is Hithpa., the word belongs to the text before
  A03092   the two "brick" passages (written as Scripture lays them out) are drawn as small right-to-left grids
Unsure, flagged in UNSURE and left as the scan reading / Sefaria has it."""
import re

# rid: (first binyan form as Sefaria has it, the name in the book)
STEM = {
    'A02976': ('אִירֵג', '*Pi.'), 'B00170': ('הִבְהָה', '*Hif.'), 'B00329': ('אִתְּבָר', '*Ithpe.'), 'B00394': ('הוֹבִישׁ', '*Hif.'),
    'B00436': ('אִתְבְּזֵי', '*Ithpe.'), 'B00461': ('נִבְזַק', '*Nif.'), 'B00484': ('אַבְחַר', '*Af.'), 'B00612': ('בַּיֵּיל', '*Pa.'),
    'B00635': ('בֹּונֵן', '*Polel'), 'B00881': ('הִבְלִים', '*Hif.'), 'B01216': ('אַבְרֵיז', '*Af.'), 'C00121': ('אַגְבַּע', '*Af.'),
    'C00166': ('גֹּדֵד', '*Polel'), 'C00984': ('הוּגְלָשׁ', '*Hof.'), 'D00264': ('אַדְוֵיל', '*Af.'), 'E00076': ('הֶהֱגִין', '*Hif.'),
    'G00102': ('הִזְהִים', '*Hif.'), 'H00256': ('אָחֵיד', '[Af.'), 'H01206': ('אִתְחַמֵּס', '*Ithpa.'), 'H01218': ('חִמֵּר', '[Pi.'),
    'H01577': ('הָחֳרָב', '*Hof.'), 'H01769': ('חָרֵיר', '[Pa.'), 'I00643': ('אַטְפֵי', '*Af.'), 'J00316': ('יַטֵּי', '*Pa.'),
    'J00501': ('יוּפָּה', '*Pu.'), 'K00807': ('כִּמֵּן', '*Pi.'), 'K01392': ('כַּתַּשׁ', '*Pa.'), 'M00395': ('אִתְמוֹגֵג', '*Ithpol.'),
    'N00176': ('הוּגָּע', '*Hof.'), 'N00238': ('אִינְּדִיף', '*Ithpe.'), 'N01193': ('הִנְקָה', '*Hif.'), 'O00940': ('הִסְתַּכֵּר', '*Hithpa.'),
    'P00105': ('עִגֵּן', '*Pi.'), 'P00160': ('אַעְדִּיק', '*Af.'), 'P00326': ('הֵעִיק', '[Hif.'), 'P00904': ('עַמְעֵם', '*Palp.'),
    'Q01474': ('הִפְקִיחַ', '*Hif.'), 'R00262': ('צוֹתֵת', '*Polel'), 'R00756': ('אַצְרִיחַ', '*Af.'), 'S00150': ('נִקְדָּם', '[Nif.'),
    'S01318': ('הִתְקַלֶּה', '*Hithpa.'), 'T00084': ('רַבֵּי', 'Pa.'), 'T00766': ('הִרְכִּיךְ', '[Hif.'), 'T00918': ('אִירְעַץ', '*Ithpe.'),
    'T00979': ('הִתְרַצֵּחַ', '*Hithpa.'), 'T01092': ('אִתְרְשֵׁים', '*Ithpe.'), 'U00161': ('אִסְתַּבַּע', '*Ithpa.'), 'V00573': ('תַּלֵּג', '*Pa.'),
    'V01044': ('אַתְרִיף', '*Af.'),
}
# host rid: (form in the fake binyan, headword of the new entry, alternative headwords, text to cut from the start of its first definition)
SPLIT = {
    'P01197': ('עָקַם', 'עָקַם', [], None),
    'K01002': ('כְּפוּשָׁה', 'כְּפוּשָׁה', [], None),
    'U00230': ('שׁוֹגֵם', 'שֶׁגֶם', ['שׁוֹגֵם'], r'^\)\s*<a[^>]*>שֶׁגֶם</a>\s*'),
    'D01003': ('דְּקִילִין', '*דְּקִילִין', ['דְּקִילָן'], None),
    'N01268': ('נ', 'נרווד', [], r'^<span dir="rtl">רווד</span>'),
}
UNSURE = {
    'T00084': "Pa. or *Pa.: the start of the line was cut off in the scan",
    'N01268b': "headword נרווד inferred from the split (scan of p. 937 not checked)",
    'D01003b': "scan of p. 319 not checked",
    'A01021': "Sefaria has *Nif. for הֶאֱחִיז, which looks like Hif.; not checked against the scan, left as is",
}
BRICK = {   # A03092, p. 119: (text as Sefaria runs it together, rows of cells, right to left; cells offset like bricks)
    'A03092': [
        ('ויאמרו לאמר\tאשירה לד׳ כי גאה גאה\tסוסורכבו רמה בים\tעזי וזמרת יה ויהי לי',
         [['ויאמרו לאמר', 'אשירה לד׳ כי גאה גאה', 'סוס'], ['ורכבו רמה בים', 'עזי וזמרת יה ויהי לי']], True),
        ('פרשנדתא\tואתדלפון\t<span dir="rtl">ואת</span>',
         [['פרשנדתא', 'ואת'], ['דלפון.', 'ואת']], False),
    ],
}

def _binyans(ss):
    for s in ss or []:
        if isinstance(s, dict):
            if s.get('grammar'): yield s
            yield from _binyans(s.get('senses'))

def _nolatin(g): return not re.search('[A-Za-z]', g.get('verbal_stem', ''))

def brick_html(rows, offset):
    out = []
    for k, row in enumerate(rows):
        cls = 'jbr'
        out.append(f'<span class="{cls}">' + ''.join(f'<span dir="rtl">{c}</span>' for c in row) + '</span>')
    return f'<span class="jbrick{"" if offset else " cols"}" dir="rtl">' + ''.join(out) + '</span>'

def apply(E):
    """fix the entries in E (rid -> Sefaria entry) in place; returns {new rid: host rid} for the split-off entries"""
    done, new = [], {}
    for rid, (form, name) in STEM.items():
        if rid not in E: continue
        hit = [s for s in _binyans(E[rid]['content'].get('senses')) if _nolatin(s['grammar'])
               and (s['grammar'].get('binyan_form') or [''])[0].strip() == form]
        if len(hit) == 1: hit[0]['grammar']['verbal_stem'] = name; done.append(rid)
        elif not any(s['grammar'].get('verbal_stem') == name for s in _binyans(E[rid]['content'].get('senses'))):
            raise SystemExit(f'jas_fix: binyan {form} not found in {rid}')
    for host, (form, hw, alts, cut) in SPLIT.items():
        if host not in E: continue
        ss = E[host]['content']['senses']
        k = next((i for i, s in enumerate(ss) if isinstance(s, dict) and s.get('grammar') and _nolatin(s['grammar'])
                  and (s['grammar'].get('binyan_form') or [''])[0].strip() == form), None)
        if k is None: raise SystemExit(f'jas_fix: merged entry {form} not found in {host}')
        moved = ss[k:]; E[host]['content']['senses'] = ss[:k]
        body = list(moved[0].get('senses') or []) + moved[1:]     # the fake binyan's own senses, then any later sections
        if cut and body and body[0].get('definition'):
            body[0] = dict(body[0], definition=re.sub(cut, '', body[0]['definition']).lstrip())
        nid = host + 'b'
        E[nid] = {'headword': hw, 'alt_headwords': alts, 'rid': nid, 'content': {'senses': body}, 'fix': 'split from ' + host}
        new[nid] = host
    if 'U00230b' in E:   # its "(preced.)" points to the entry before it in the book, שָׁגַם (Sefaria links it to שֵׁגָל)
        b = E['U00230b']['content']['senses']
        if b and b[0].get('definition'):
            b[0]['definition'] = b[0]['definition'].replace('href="/Jastrow,_שֵׁגָל.1" data-ref="Jastrow, שֵׁגָל 1">preced.', 'href="/Jastrow,_שָׁגַם.1" data-ref="Jastrow, שָׁגַם 1">preced.')
    if 'O01711' in E:
        ss = E['O01711']['content']['senses']
        k = next((i for i, s in enumerate(ss) if isinstance(s, dict) and (s.get('grammar') or {}).get('verbal_stem') == 'נִסְתַּר.'), None)
        if k is not None:
            ss[k]['grammar']['verbal_stem'] = 'Hithpa.'
    return new

def fix_html(rid, html):
    """changes made to the rendered entry (after jas_build has turned it into the pop-up's HTML)"""
    for old, rows, offset in BRICK.get(rid, []):
        if old in html: html = html.replace(old, brick_html(rows, offset))
    if rid == 'O01711':   # show נִסְתַּר, before the binyan name, as in the book
        html = html.replace('<b class="jg">Hithpa.</b> <span dir="rtl">הִסְתַּתֵּר</span>', '<span dir="rtl">נִסְתַּר</span>, <b class="jg">Hithpa.</b> <span dir="rtl">הִסְתַּתֵּר</span>', 1)
    return html
