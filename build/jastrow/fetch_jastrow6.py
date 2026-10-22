#!/usr/bin/env python3
"""
Fetch the 9 Jastrow entries Sefaria's word search does not return, by their page name
(the way https://www.sefaria.org/Jastrow,_<headword>.1 opens them). 9 entries, under a minute.
Run:  python3 fetch_jastrow6.py      Then attach  jastrow-pages-6.json  in the Claude chat.
"""
import json, os, time, urllib.parse, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
UA = "onkelos-chumash glossary (github.com/menachemshapiro/onkelos-chumash); 9 Jastrow entries by page name"
# entry id -> its headword as Sefaria's neighbouring entries name it
PAGES = {
"D00963": [
"דפליסט׳"
],
"E00856": [
"הַרְטָבָה׳"
],
"N00665": [
"ניכו׳"
],
"N01331": [
"נְשַׁם"
],
"Q01633": [
"פרווטי׳",
"פרווטי"
],
"Q01962": [
"פַּרְפֵּר"
],
"S02155": [
"קַרְצֵף"
],
"T00138": [
"רְבַץ"
],
"U01398": [
"שַׁלְשֵׁל I"
]
}
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404: return {"error": 404}
            time.sleep(8 * (attempt + 1))
        except Exception as e: time.sleep(8)
    return {"error": "failed"}
out = {}
for rid, names in PAGES.items():
    out[rid] = {}
    for hw in names:
        ref = "Jastrow, " + hw + " 1"
        for name, url in [("v3", "https://www.sefaria.org/api/v3/texts/" + urllib.parse.quote(ref)),
                          ("v1", "https://www.sefaria.org/api/texts/" + urllib.parse.quote(ref) + "?context=0&commentary=0")]:
            out[rid][name + " " + hw] = get(url); time.sleep(0.6)
        ok = any(isinstance(v, dict) and not v.get("error") and (v.get("versions") or v.get("text") or v.get("he")) for v in out[rid].values())
        if ok: break
    print(rid, names[0] if names else "?", "ok" if ok else "not found")
json.dump(out, open(os.path.join(HERE, "jastrow-pages-6.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("Attach jastrow-pages-6.json in the Claude chat.")
