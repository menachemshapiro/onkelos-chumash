#!/usr/bin/env python3
"""
Fetch the 26 Jastrow entries Sefaria's word search does not return, by their page name
(the way https://www.sefaria.org/Jastrow,_<headword>.1 opens them). 26 entries, about a minute.
Run:  python3 fetch_jastrow5.py      Then attach  jastrow-pages-5.json  in the Claude chat.
"""
import json, os, time, urllib.parse, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
UA = "onkelos-chumash glossary (github.com/menachemshapiro/onkelos-chumash); 26 Jastrow entries by page name"
# entry id -> its headword as Sefaria's neighbouring entries name it
PAGES = {
"B00002": [
"ב׳"
],
"E00433": [
"הימני׳"
],
"G00527": [
"זְמַם I"
],
"G00643": [
"זְקַן"
],
"I00676": [
"טְפַף"
],
"K00107": [
"כִּדְ׳ כַּדְבוּבָא"
],
"L00001": [
"ל׳"
],
"M02444": [
"מְקַק"
],
"M02697": [
"מְרַךְ"
],
"M03049": [
"מתיב"
],
"P00766": [
"עֲלַב"
],
"P00918": [
"עֲמַק"
],
"P01210": [
"עֲקַף"
],
"Q00078": [
"פִּגְמִין"
],
"Q02043": [
"פְּרַת I"
],
"R00217": [
"צוּף ²"
],
"S00733": [
"קְטַט"
],
"S02268": [
"קְשַׁשׁ I"
],
"T00146": [
"רַבְרֵב"
],
"T00773": [
"רְכַס"
],
"T00942": [
"רְפַט"
],
"T00958": [
"רְפַף"
],
"U00208": [
"שְׂגַב"
],
"U01492": [
"שְׁמַם"
],
"U01497": [
"שְׁמֵן"
],
"U01626": [
"שׁע׳"
],
"V00774": [
"תְּעֵב"
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
json.dump(out, open(os.path.join(HERE, "jastrow-pages-5.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("Attach jastrow-pages-5.json in the Claude chat.")
