# Chumash with Onkelos

**Open it:** https://menachemshapiro.github.io/onkelos-chumash/

A study page for learning Targum Onkelos alongside the Chumash, Bereishis through Vezos Haberachah. Each pasuk is split into short clauses, with the Hebrew, Onkelos and the English side by side, so you can see which Aramaic words translate which Hebrew words. Rashi follows each pasuk.

## Features

- **Highlights.** Where Onkelos departs from a word-for-word translation, the Aramaic and the English that explains it are highlighted.
- **Three English modes.** *Combined* (Metsudah with Onkelos's wording in [brackets]), *Plain* (follows the Hebrew), *Onkelos* (rewritten to follow the Targum, Onkelos's wording in bold).
- **Onkelos word by word.** A drop-down under each line showing which English renders each Aramaic word, with short notes.
- **Targum glossary (beta).** Tap any Aramaic word for its parts, root, form, meaning in this pasuk and dictionary entry.
- **Jastrow.** From a glossary card, open the word's entry in Jastrow's dictionary (matched automatically).
- **Navigation.** Pick a sefer, parsha, aliyah, perek or pasuk, or type a reference like `32:13` or `Vayechi 49:11`.
- **Your layout.** Turn te'amim, Targum, English and Rashi on or off; choose fonts and sizes.
- **Export** a parsha, aliyah, perek or range of pesukim as PDF or Word.
- **Home-screen app.** In Safari, *Share → Add to Home Screen*. Works offline after the first visit.

Tap **?** on the page for a short guide.

> **The glossary is in beta.** It was written with the help of an AI (Claude) and checked by script, not by a scholar, so it will have mistakes, especially in rare words. Don't rely on it where a mistake matters.

## Sources

| Text | Source | License |
|---|---|---|
| Hebrew with te'amim | Tanach with Ta'amei Hamikra (tanach.us), via Sefaria | Public domain |
| Targum Onkelos | Sifsei Chachomim Chumash, Metsudah Publications, 2009, via Sefaria | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) |
| English | Metsudah Chumash, Metsudah Publications, 2009, via Sefaria | [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) |
| Rashi | Sefaria's merged text (Rosenbaum–Silbermann 1929–34; Metsudah Rashi Chumash 2009; *On Your Way*) | Public domain / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Jastrow's Dictionary | M. Jastrow, *A Dictionary of the Targumim, the Talmud Babli and Yerushalmi, and the Midrashic Literature* (1903), via Sefaria's API | Public domain |
| Glossary | Written for this project; a few dozen hard words checked against the Comprehensive Aramaic Lexicon (logged in `build/cal-log.json`) | — |
| Fonts | Mekorot Rashi (LPPL 1.3c), Mekorot Vilna (GPL), Google Fonts (OFL) | as listed |

The English was reordered in some pesukim so each Onkelos rendering sits beside its clause, and clear typos were fixed. Every change and decision is listed in [`DECISIONS.md`](DECISIONS.md).

**Non-commercial use only**, as required by the CC BY-NC license of the Onkelos and English texts.

## For developers

The page is maintained in a Claude conversation, published on claude.ai, then pushed here.

| Path | What it is |
|---|---|
| `index.html` | The page, wrapped as a home-screen app |
| `p/*.json` | Each parsha's text (Hebrew, Targum, English, Rashi, Onkelos English), loaded as needed |
| `g/*.json` | The Targum glossary per parsha |
| `j/*.json` | Jastrow entries for the glossary, loaded when opened |
| `manifest.webmanifest`, `sw.js`, `icons/` | App settings, offline support, icons |
| `DECISIONS.md` | Every compromise and decision in aligning and presenting the texts |
| `build/` | Build scripts and hand-set fixes (`build_page.py`, `align.py`, `ovr-*.json`), the glossary (`gloss_build.py`, `gl/`), and the Onkelos English (`eo-align/`, `eo_check.py`, `eo_merge.py`) |
| `sources/` | Source texts as downloaded from Sefaria |
