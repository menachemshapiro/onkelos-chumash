#!/usr/bin/env python3
"""
Check the 32 Jastrow entries Sefaria did not return (round 4, a quick check: about 100 lookups, under 2 minutes).
Run:  python3 fetch_jastrow4.py      Then attach  jastrow-check-4.json  in the Claude chat.
For each missing entry it asks Sefaria under the headword, the headword without vowels, a corrected spelling where the
2018 headword was garbled, and the entry just before it (in case Sefaria merged the two). It keeps every Jastrow result.
"""
import json, os, time, urllib.parse, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
UA = "onkelos-chumash glossary (github.com/menachemshapiro/onkelos-chumash); check of 32 missing Jastrow entries"
Q = {
"B00002": [
"ב'",
"ב"
],
"B00761": [
"בית יוני",
"בית־יוני",
"ביתיוני",
"ביתור"
],
"D00327": [
"דּוּקָא",
"דוקא",
"דַּוְקָא"
],
"E00433": [
"הימני",
"הימני'",
"הֵימָנוּתָא"
],
"G00527": [
"זְמַם",
"זמם",
"זָמַם"
],
"G00643": [
"זְקַן",
"זקן",
"זָקֵן"
],
"H01091": [
"חֶלְמוֹן",
"חלמון",
"(הֶלְ') חֶלְמוֹן",
"הלחלמון",
"חֶלְמָה"
],
"I00676": [
"טְפַף",
"טפף",
"טָפַף"
],
"K00107": [
"כַּדְבוּבָא",
"כדבובא",
"כִּדְ' כַּדְבוּבָא",
"כדכדבובא",
"כַּדְבֵּב"
],
"L00001": [
"ל'",
"ל"
],
"M02444": [
"מְקַק",
"מקק",
"מָקַק"
],
"M02697": [
"מְרַךְ",
"מרך",
"מָרַךְ"
],
"M03049": [
"מתיב",
"מַתְּיָא"
],
"P00766": [
"עֲלַב",
"עלב",
"עָלַב"
],
"P00918": [
"עֲמַק",
"עמק",
"עָמַק"
],
"P01210": [
"עֲקַף",
"עקף",
"עָקַף"
],
"Q00078": [
"פִּגְמִין",
"פגמין",
"פְּגָמָא"
],
"Q02043": [
"פְּרַת",
"פרת",
"פָּרַת"
],
"R00217": [
"צוּף",
"צוף"
],
"S00377": [
"קומי",
"קומ־",
"קומ",
"קוֹם"
],
"S00733": [
"קְטַט",
"קטט",
"קָטַט"
],
"S02268": [
"קְשַׁשׁ",
"קשש",
"קָשַׁשׁ"
],
"T00146": [
"רַבְרֵב",
"רברב",
"רִבְרֵב"
],
"T00773": [
"רְכַס",
"רכס",
"רָכַס"
],
"T00942": [
"רְפַט",
"רפט",
"רָפַט"
],
"T00958": [
"רְפַף",
"רפף",
"רָפַף"
],
"U00208": [
"שְׂגַב",
"שגב",
"שָׂגַב"
],
"U01492": [
"שְׁמַם",
"שמם",
"שָׁמֵם"
],
"U01497": [
"שְׁמֵן",
"שמן",
"שָׁמֵן"
],
"U01626": [
"שׁע'",
"שע",
"שַׁע"
],
"V00593": [
"תְּלִישָׁה",
"תלישה",
"תְּלִ",
"תל",
"תְּלֵיסַר"
],
"V00774": [
"תְּעֵב",
"תעב",
"תָּעַב"
]
}
def fetch(word):
    url = "https://www.sefaria.org/api/words/" + urllib.parse.quote(word) + "?always_consonants=1"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404: return []
            time.sleep(10 * (attempt + 1))
        except Exception: time.sleep(10)
    return []
out, asked = {}, {}
for rid, qs in Q.items():
    out[rid] = {}
    for q in qs:
        if q not in asked:
            data = fetch(q); time.sleep(0.6)
            asked[q] = [d for d in (data if isinstance(data, list) else []) if d.get("parent_lexicon") == "Jastrow Dictionary"]
        out[rid][q] = asked[q]
    print(rid, "found" if any(d.get("rid") == rid for v in out[rid].values() for d in v) else "not found")
json.dump(out, open(os.path.join(HERE, "jastrow-check-4.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("Attach jastrow-check-4.json in the Claude chat.")
