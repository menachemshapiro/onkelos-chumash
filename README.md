# Chumash with Onkelos

A clause-by-clause study page for the whole Chumash: the Hebrew text with te'amim, Targum Onkelos and the Metsudah English side by side, with Rashi under each pasuk, aliyah and perek navigation, a go-to box, and PDF / Word / web-page export.

**Open it:** https://menachemshapiro.github.io/onkelos-chumash/ (once GitHub Pages is turned on).
On an iPhone, open it in Safari and choose **Share → Add to Home Screen** to use it as an app. After the first visit every parsha is kept on the phone, so it also works offline.

## What's here

| Path | What it is |
|---|---|
| `index.html` | The page (the same page published on claude.ai, wrapped as a home-screen app) |
| `p/*.json` | The text of each parsha: Hebrew, Targum, English and Rashi, fetched as needed |
| `manifest.webmanifest`, `sw.js`, `icons/` | Home-screen app settings, offline support and icons |
| `DECISIONS.md` | Every compromise and decision made in aligning and presenting the texts |
| `build/` | The scripts and hand-set alignment fixes that produce the page (`build_page.py`, `align.py`, `reorder.py`, `fixes.py`, `ovr-*.json`, ...) |
| `sources/` | The source texts as downloaded from Sefaria |

The page is maintained in a Claude conversation; each update is published there and pushed here.

## Sources and licenses

- Hebrew text with te'amim: Tanach with Ta'amei Hamikra (tanach.us), via Sefaria. Public domain.
- Targum Onkelos: Sifsei Chachomim Chumash, Metsudah Publications, 2009, via Sefaria. [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
- English: Metsudah Chumash, Metsudah Publications, 2009 [with Onkelos translation], via Sefaria. [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
- Rashi: Sefaria's merged text, from *Pentateuch with Rashi's Commentary*, ed. M. Rosenbaum and A.M. Silbermann, 1929–1934 (public domain); Rashi Chumash, Metsudah Publications, 2009 ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)); and *On Your Way* (public domain).
- Fonts: Mekorot Rashi (LPPL 1.3c) and Mekorot Vilna (GPL), based on Culmus fonts; Google Fonts (SIL Open Font License).

The texts were divided into clauses and aligned; some English was reordered so bracketed Onkelos renderings sit beside their clauses, and clear typos were corrected (see `DECISIONS.md`). **Non-commercial use only**, as required by the CC BY-NC license of the Onkelos and English texts.
