#!/usr/bin/env python3
"""
Download Sefaria's current text for every Jastrow entry we don't have yet (__N__ entries),
so that, together with what we already downloaded, we have the whole dictionary.

How to run (needs Python 3, nothing else to install):
    python3 fetch_jastrow_all.py          (on Windows: py fetch_jastrow_all.py)

How it works, one request at a time with a pause between requests:
  1. asks Sefaria's dictionary search (https://www.sefaria.org/api/words/...) for each entry's headword;
     one search often brings back several entries, so it skips entries that have already come back;
  2. tries the other spellings of entries still missing;
  3. opens whatever is still missing by its page name (https://www.sefaria.org/Jastrow,_<headword>.1),
     the way we got the entries the search doesn't return.
Expect about 2 hours. You can stop it any time (Ctrl+C) or let the computer sleep: run it again and it
continues where it stopped (keep jastrow-progress-all.jsonl next to it).
When it finishes it writes  jastrow-all.json  next to this script. Attach that file (and, if it's
not too big, jastrow-progress-all.jsonl) in the Claude chat.
"""
import json, os, sys, time, urllib.parse, urllib.request, urllib.error

PAUSE = 0.5          # seconds between requests, to go easy on Sefaria's server
HERE = os.path.dirname(os.path.abspath(__file__))
PROGRESS = os.path.join(HERE, "jastrow-progress-all.jsonl")
OUT = os.path.join(HERE, "jastrow-all.json")
UA = "onkelos-chumash (github.com/menachemshapiro/onkelos-chumash); completing a copy of Jastrow, one request at a time"

# entry id -> {"q": [search words, first the headword], "n": [page names to try]}
WANT = __WANT__
# names Sefaria gives each entry, taken from the entries before and after it that we already have
KNOWN_NAMES = __NAMES__

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (400, 404): return None
            wait = 30 * (attempt + 1) if e.code == 429 else 5 * (attempt + 1)
            print(f"  server said {e.code}; waiting {wait}s and trying again"); time.sleep(wait)
        except Exception as e:
            print(f"  network problem ({e}); waiting 10s and trying again"); time.sleep(10)
    raise SystemExit("Too many failures in a row. Check your internet connection and run the script again; it will continue where it stopped.")

def search(word):
    data = get("https://www.sefaria.org/api/words/" + urllib.parse.quote(word) + "?always_consonants=1")
    out = []
    for d in data if isinstance(data, list) else []:
        if d.get("parent_lexicon") == "Jastrow Dictionary":
            d.pop("parent_lexicon_details", None); out.append(d)
    return out

def page(name):
    data = get("https://www.sefaria.org/api/v3/texts/" + urllib.parse.quote("Jastrow, " + name + " 1"))
    try:
        t = data["versions"][0]["text"]
        if t and any(x.strip() for x in (t if isinstance(t, list) else [t])): return t
    except Exception: pass
    return None

def neighbour(rid, step):
    try: return rid[0] + "%05d" % (int(rid[1:]) + step)
    except ValueError: return None

def main():
    asked, got, pages = set(), {}, {}
    if os.path.exists(PROGRESS):
        with open(PROGRESS, encoding="utf-8") as f:
            for line in f:
                try: rec = json.loads(line)
                except Exception: continue
                if "q" in rec:
                    asked.add(rec["q"])
                    for d in rec["r"]: got[d["rid"]] = d
                elif "p" in rec:
                    asked.add("page:" + rec["name"])
                    if rec.get("text"): pages[rec["p"]] = {"name": rec["name"], "text": rec["text"]}
    have = lambda r: r in got or r in pages
    print(f"{len(WANT)} entries wanted; {sum(1 for r in WANT if have(r))} already downloaded")
    t0, n = time.time(), 0
    def tick(i, total):
        if i % 100 == 0 or i == total:
            left = (time.time() - t0) / max(n, 1) * (total - i)
            print(f"  {i}/{total} done, {sum(1 for r in WANT if have(r))} of {len(WANT)} entries found, about {int(left // 60)} min left this pass")
    with open(PROGRESS, "a", encoding="utf-8") as f:
        for rnd in range(3):                       # pass 1: headwords; passes 2-3: other spellings
            todo = [w for w in WANT if not have(w) and len(WANT[w]["q"]) > rnd and WANT[w]["q"][rnd] not in asked]
            if not todo: continue
            print(f"pass {rnd + 1}: up to {len(todo)} searches")
            for i, rid in enumerate(todo, 1):
                q = WANT[rid]["q"][rnd]
                if have(rid) or q in asked: tick(i, len(todo)); continue
                r = search(q); asked.add(q); n += 1
                f.write(json.dumps({"q": q, "r": r}, ensure_ascii=False) + "\n"); f.flush()
                for d in r: got[d["rid"]] = d
                tick(i, len(todo)); time.sleep(PAUSE)
        # pass 4: by page name, for what the search doesn't return
        todo = [w for w in WANT if not have(w)]
        if todo: print(f"pass 4: {len(todo)} entries by page name")
        for i, rid in enumerate(todo, 1):
            names = list(KNOWN_NAMES.get(rid, []))
            a, b = got.get(neighbour(rid, -1)), got.get(neighbour(rid, 1))
            if a and a.get("next_hw"): names.append(a["next_hw"])
            if b and b.get("prev_hw"): names.append(b["prev_hw"])
            names += WANT[rid]["n"]
            for name in dict.fromkeys(x for x in names if x):
                if "page:" + name in asked: continue
                t = page(name); asked.add("page:" + name); n += 1
                f.write(json.dumps({"p": rid, "name": name, "text": t}, ensure_ascii=False) + "\n"); f.flush()
                time.sleep(PAUSE)
                if t: pages[rid] = {"name": name, "text": t}; break
            tick(i, len(todo))
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"source": "Sefaria API, Jastrow Dictionary (London, Luzac, 1903; public domain)",
                   "fetched": time.strftime("%Y-%m-%d"), "entries": got, "pages": pages}, f, ensure_ascii=False)
    found = sum(1 for r in WANT if have(r))
    print(f"Finished: {found} of {len(WANT)} wanted entries found ({len(got)} entries from the search, {len(pages)} by page name), saved to {OUT}")
    missing = [r for r in WANT if not have(r)]
    if missing: print(f"{len(missing)} not found: " + " ".join(missing[:40]) + (" ..." if len(missing) > 40 else ""))
    print("Attach jastrow-all.json in the Claude chat.")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\nStopped. Run the script again to continue.")
