#!/usr/bin/env python3
"""
Download Sefaria's current text for the Jastrow entries the Chumash with Onkelos site uses
but so far has only from Sefaria's 2018 data (round 3; 94 entries).

How to run (needs Python 3, nothing else to install):
    python3 fetch_jastrow3.py          (on Windows: py fetch_jastrow3.py)

It asks Sefaria's public dictionary API (https://www.sefaria.org/api/words/...) for each entry's
headword, one request at a time with a pause between requests, and keeps only the Jastrow entries
we want (matched by their id). If an entry is not found under its headword, it tries the entry's
other spellings. Expect a few minutes. If it stops, run it again: it picks up where it left off.
When it finishes it writes  jastrow-lookups-3.json  next to this script. Attach that file in the Claude chat.
"""
import json, os, time, urllib.parse, urllib.request, urllib.error

PAUSE = 0.5          # seconds between requests, to go easy on Sefaria's server
HERE = os.path.dirname(os.path.abspath(__file__))
PROGRESS = os.path.join(HERE, "jastrow-progress-3.jsonl")
OUT = os.path.join(HERE, "jastrow-lookups-3.json")
UA = "onkelos-chumash glossary (github.com/menachemshapiro/onkelos-chumash); round 3, entries used by the site"

# entry id -> [headword, other spellings...]
WANT = {
"A00075": [
"אֲבוּנָא",
"אֲבוּנָה"
],
"A00234": [
"אגאלוגין",
"אגאליגין"
],
"A00304": [
"אגלין"
],
"A00458": [
"אַדְרִיאָנוֹס"
],
"A00662": [
"אולוגלוגין"
],
"A00773": [
"אוֹנְקְלוֹס",
"אָנְקְלוֹס"
],
"A01392": [
"אִינְקוֹרָא",
"אִנְקוֹרָא"
],
"A01723": [
"אָכְסִיגָרוֹן"
],
"A02033": [
"אמלוגין"
],
"A02250": [
"אַנְלוֹגִין"
],
"A02642": [
"אפוקלוס",
"אפוקליס"
],
"A02776": [
"אפקוליס"
],
"A02869": [
"אצטרא"
],
"A02997": [
"ארגסטירין"
],
"B00226": [
"בּוּטָא"
],
"B01205": [
"בְּרוּקְלֵי"
],
"C01240": [
"גְּרַבְתָּא"
],
"C01241": [
"גְּרַבְתָּן"
],
"D00963": [],
"D01047": [
"דַּרְדַּנְיָא"
],
"E00169": [
"הִדְרָקוֹן"
],
"E00307": [
"הֶחְלֵט"
],
"E00665": [
"הִנְדְּקָאֵי"
],
"E00856": [],
"I00148": [
"טוֹטַפְרָאוֹת"
],
"I00278": [
"טֹטַפְרָאוֹת"
],
"I00289": [
"טטרפאות"
],
"J00506": [
"יְפֵיפָה"
],
"J00554": [
"יָקַב"
],
"J00619": [
"יְרוּשַׁלְמִי"
],
"K01212": [
"כַּרְכְּמִישָׁא"
],
"L00425": [
"ליגגין"
],
"L00428": [
"ליגנין"
],
"M00800": [
"מַחְבְּטָא"
],
"M01654": [
"מְמוּשׁ"
],
"M02706": [
"מָרְכְּיוֹתָא"
],
"N00440": [
"נִזְיֵי"
],
"N00441": [
"נִזְיָיתָא"
],
"N00639": [
"נִיוְתִּי"
],
"N00665": [],
"N01088": [
"נַפְתּוֹחָא",
"נַפְתּוֹחָאָה"
],
"N01089": [
"נִפְתִּי",
"נִפְתַּיי",
"נִפְתָּיָיא",
"… יָיה"
],
"N01200": [
"נְקִידָא"
],
"N01331": [
"נְשַׁם"
],
"O00138": [
"סְגִיעַ"
],
"O00506": [
"סטרגלים"
],
"O00840": [
"סִירוֹנִי",
"סִירוֹנִית"
],
"O01039": [
"סָלַרְיָא"
],
"O01242": [
"סנירתא"
],
"P00087": [
"עָגִיל"
],
"P00286": [
"עוֹמְקָן"
],
"P00287": [
"עוּמְקָנָא"
],
"P01287": [
"עַרְבְּלָאִין"
],
"Q00011": [
"פָּאטִי"
],
"Q00015": [
"פָּאנִיקְנִין",
"פאנקין"
],
"Q00017": [
"פאנקין"
],
"Q00126": [
"פדיעא"
],
"Q00201": [
"פּוֹיְיטָן",
"פּוֹיְיטָנָא"
],
"Q00283": [
"פונקין"
],
"Q00290": [
"פּוּסְיָאנִי",
"פּוּסְיוֹנִי",
"פּוּסְיָינִי"
],
"Q01175": [
"פַּנְטֵי"
],
"Q01225": [
"פסאני"
],
"Q01262": [
"פַּסְטִי"
],
"Q01273": [
"פִּסְיָאנִי"
],
"Q01391": [
"פַּעְפּוּעָא"
],
"Q01560": [
"פרגילנין"
],
"Q01565": [
"פְּרַגְלִינִין"
],
"Q01633": [],
"Q01936": [
"פַּרְסָנִית"
],
"Q01962": [
"פַּרְפֵּר"
],
"Q02001": [
"פרקילינין"
],
"Q02007": [
"פרקלינין",
"פרקלנין"
],
"R00472": [
"צִיתְרֵי"
],
"S00082": [
"קבסיו",
"קִבְסַיי"
],
"S00271": [
"קוזות"
],
"S00519": [
"קוּפְסַאי"
],
"S00878": [
"קֵיוָא"
],
"S01038": [
"קִינְטֵירָא",
"קִינְטֵרָא"
],
"S01111": [
"קִיפָלִין"
],
"S01113": [
"קיפלירוסים",
"קיפלרין"
],
"S01197": [
"קירצוד"
],
"S01205": [
"קִישׁ"
],
"S01635": [
"קַסְדָּא",
"קַסְדָּה"
],
"S01722": [
"קְפוּצַאי"
],
"S02155": [
"קַרְצֵף"
],
"T00138": [
"רְבַץ"
],
"T00446": [
"רוֹרְבָא",
"רוֹרְבָנָא",
"רוֹרבָנוּתָא"
],
"T00683": [
"ריפע"
],
"T01124": [
"רָתְחָא"
],
"U00459": [
"שׁוּמְשׁוּם"
],
"U00860": [
"שִׁיחָה"
],
"U01398": [
"שַׁלְשֵׁל"
],
"U01902": [
"שֹׁקֶת"
],
"V00393": [
"תַּחְתּוֹן"
]
}

def fetch(word):
    url = "https://www.sefaria.org/api/words/" + urllib.parse.quote(word) + "?always_consonants=1"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            if e.code == 404: return []
            wait = 30 * (attempt + 1) if e.code == 429 else 5 * (attempt + 1)
            print(f"  server said {e.code}; waiting {wait}s and trying again"); time.sleep(wait)
        except Exception as e:
            print(f"  network problem ({e}); waiting 10s and trying again"); time.sleep(10)
    else:
        raise SystemExit("Too many failures in a row. Check your internet connection and run the script again; it will continue where it stopped.")
    if not isinstance(data, list): return []
    out = []
    for d in data:
        if d.get("parent_lexicon") == "Jastrow Dictionary":
            d.pop("parent_lexicon_details", None); out.append(d)
    return out

def main():
    asked, got = set(), {}
    if os.path.exists(PROGRESS):
        with open(PROGRESS, encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line); asked.add(rec["q"])
                    for d in rec["r"]:
                        if d.get("rid") in WANT: got[d["rid"]] = d
                except Exception: pass
    print(f"{len(WANT)} entries wanted; {len(got)} already downloaded")
    t0, n = time.time(), 0
    with open(PROGRESS, "a", encoding="utf-8") as f:
        for rnd in range(3):                       # headword first, then other spellings
            todo = []
            for rid, hs in WANT.items():
                if rid in got or len(hs) <= rnd: continue
                if hs[rnd] not in asked and hs[rnd] not in todo: todo.append(hs[rnd])
            if not todo: continue
            print(f"pass {rnd + 1}: {len(todo)} lookups")
            for i, q in enumerate(todo, 1):
                r = fetch(q); asked.add(q); n += 1
                f.write(json.dumps({"q": q, "r": r}, ensure_ascii=False) + "\n"); f.flush()
                for d in r:
                    if d.get("rid") in WANT: got[d["rid"]] = d
                if i % 100 == 0 or i == len(todo):
                    left = (time.time() - t0) / n * (len(todo) - i)
                    print(f"  {i}/{len(todo)} done, {len(got)} entries found, about {int(left // 60)} min left")
                time.sleep(PAUSE)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"source": "Sefaria API, Jastrow Dictionary (London, Luzac, 1903; public domain)",
                   "fetched": time.strftime("%Y-%m-%d"), "queries": {}, "entries": got}, f, ensure_ascii=False)
    print(f"Finished: {len(got)} of {len(WANT)} entries saved to {OUT}")
    missing = [r for r in WANT if r not in got]
    if missing: print(f"{len(missing)} not found on Sefaria (the site keeps the 2018 text for those).")
    print("Attach jastrow-lookups-3.json in the Claude chat.")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\nStopped. Run the script again to continue.")
