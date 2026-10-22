#!/usr/bin/env python3
"""
Download Sefaria's current text for the Jastrow entries the Chumash with Onkelos site uses
but so far has only from Sefaria's 2018 data (round 3; 0 entries).

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
WANT = {}

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
