#!/usr/bin/env python3
"""Download Sefaria's two Jastrow abbreviation pages, "Jastrow, List of Abbreviations" and
"Jastrow, Hebrew or Aramaic Abbreviations" (two requests), and save them together as jastrow-abbr-list.json.
Run:  python3 fetch_abbr_list.py      Then attach jastrow-abbr-list.json in the Claude chat."""
import json, os, time, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
UA = "onkelos-chumash (github.com/menachemshapiro/onkelos-chumash); Jastrow lists of abbreviations"
out = {}
for name in ["Jastrow, List of Abbreviations", "Jastrow, Hebrew or Aramaic Abbreviations"]:
    url = "https://www.sefaria.org/api/v3/texts/" + urllib.parse.quote(name)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r: out[name] = json.loads(r.read().decode("utf-8"))
        t = out[name].get("versions", [{}])[0].get("text")
        print(name + ":", (len(t) if isinstance(t, list) else "?"), "lines")
    except Exception as e:
        out[name] = {"error": str(e)}; print(name + ": failed (" + str(e) + ")")
    time.sleep(1)
json.dump(out, open(os.path.join(HERE, "jastrow-abbr-list.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("Saved. Attach jastrow-abbr-list.json in the Claude chat.")
