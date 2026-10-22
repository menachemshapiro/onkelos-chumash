#!/usr/bin/env python3
"""Download every part of Sefaria's Jastrow that is not a dictionary entry: the Preface, the two abbreviation lists,
and any other front or back matter (addenda, etc.). First it reads the book's table of contents, then one request per part.
Run:  python3 fetch_front_matter.py      Then attach jastrow-front-matter.json in the Claude chat."""
import json, os, time, urllib.parse, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
UA = "onkelos-chumash (github.com/menachemshapiro/onkelos-chumash); Jastrow front and back matter"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read().decode("utf-8"))
    except Exception as e: return {"error": str(e)}
out = {"index": get("https://www.sefaria.org/api/v2/raw/index/Jastrow"), "parts": {}}
names = []
def walk(node):
    for n in node.get("nodes", []) or []:
        t = n.get("title") or next((x["text"] for x in n.get("titles", []) if x.get("lang") == "en" and x.get("primary")), None)
        kind = n.get("nodeType", "")
        if t and "Dictionary" not in kind: names.append(t)
        walk(n)
walk(out["index"].get("schema", {}))
for t in ["Preface", "Hebrew or Aramaic Abbreviations", "List of Abbreviations"]:   # the ones we know exist
    if t not in names: names.append(t)
print("Parts found:", ", ".join(names))
for t in names:
    ref = "Jastrow, " + t
    out["parts"][t] = get("https://www.sefaria.org/api/v3/texts/" + urllib.parse.quote(ref))
    v = (out["parts"][t].get("versions") or [{}])[0].get("text")
    print(" ", t + ":", (f"{len(v)} lines" if isinstance(v, list) else "no text" if not v else "1 block"))
    time.sleep(1)
json.dump(out, open(os.path.join(HERE, "jastrow-front-matter.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("Saved. Attach jastrow-front-matter.json in the Claude chat.")
