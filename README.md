# Chumash with Onkelos

**Open it:** https://menachemshapiro.github.io/onkelos-chumash/

A study page for learning Targum Onkelos alongside the Chumash. Every pasuk is broken into short clauses, and each clause shows the Hebrew, the Targum and the English together, so you can see exactly which Aramaic words translate which Hebrew words. Rashi follows each pasuk.

It covers the whole Torah, from Bereishis to Vezos Haberachah.

## What you can do with it

- **Read clause by clause.** The Hebrew (with te'amim), Onkelos and the Metsudah English line up phrase by phrase rather than verse by verse.
- **See where Onkelos interprets.** Where Onkelos departs from a word-for-word translation, the Aramaic is highlighted. The English that explains it is highlighted the same way, so the two are easy to match.
- **Tap any word of the Targum** to open a short card about it (see below).
- **Move around easily.** Choose a sefer, parsha, aliyah or perek, or type a reference such as לב:יג in the go-to box.
- **Read the English as Onkelos reads it.** The drop-down next to the English button switches between **Combined** (the Metsudah English with Onkelos's wording in [brackets]), **Plain** (brackets taken out, following the Hebrew) and **Onkelos** (the English rewritten to follow the Targum, with Onkelos's own wording in bold).
- **Onkelos word by word.** Turn on **Word by word** to get a drop-down under the English for each line. It shows which English renders each Aramaic word, with short notes where something needs explaining.
- **Show only what you want.** Te'amim, Targum, English and Rashi can each be turned on or off.
- **Adjust the look.** Choose fonts and sizes for the Hebrew, Targum, English and Rashi. Your choices are saved in your browser.
- **Print or save.** Export a parsha, an aliyah, a perek or a range of pesukim as a PDF or a Word document.
- **Use it as an app.** On an iPhone, open the page in Safari and choose **Share → Add to Home Screen**. After the first visit every parsha is kept on the phone, so it also works offline.
- **Report a mistake.** Each pasuk and each glossary card has a **Report a problem** button.

## The Targum glossary — beta

Tap any Aramaic word in the Targum and a card opens showing:

- the word split into its parts — prefixes such as ו and ד, the word itself, and its endings — each labeled;
- the **root**;
- the **form** (for example "verb, Pa'el, past, 3rd masc. sing." or "noun, emphatic");
- what the word means **in this pasuk**;
- the **dictionary entry** for the word.

The glossary is meant to help someone who knows Hebrew and wants to read Onkelos's Aramaic on their own.

> **The glossary is in beta and will have mistakes.** It was written word by word with the help of an AI (Claude) and checked by script, not reviewed by a scholar. A few thousand glosses have already been corrected, but errors remain, especially in rare words and in words that mean different things in different places. If something looks wrong, please use **Report a problem** on the card. Don't rely on the glossary for psak or for anything where a mistake matters.

## Where the texts come from

- **Hebrew text with te'amim:** Tanach with Ta'amei Hamikra (tanach.us), via Sefaria. Public domain.
- **Targum Onkelos:** Sifsei Chachomim Chumash, Metsudah Publications, 2009, via Sefaria. [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
- **English:** Metsudah Chumash, Metsudah Publications, 2009 [with Onkelos translation], via Sefaria. [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
- **Rashi:** Sefaria's merged text, from *Pentateuch with Rashi's Commentary*, ed. M. Rosenbaum and A.M. Silbermann, 1929–1934 (public domain); Rashi Chumash, Metsudah Publications, 2009 ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)); and *On Your Way* (public domain).
- **Glossary:** written for this project. For a few dozen hard words, meanings were checked against the Comprehensive Aramaic Lexicon (cal.huc.edu); every lookup is logged in `build/cal-log.json`.
- **Fonts:** Mekorot Rashi (LPPL 1.3c) and Mekorot Vilna (GPL), based on Culmus fonts; Google Fonts (SIL Open Font License).

To line the texts up, they were divided into clauses. In some pesukim the English was reordered so that the bracketed Onkelos renderings sit beside their own clauses, and clear typos were corrected. Every such change is listed in [`DECISIONS.md`](DECISIONS.md).

**Non-commercial use only**, as required by the CC BY-NC license of the Onkelos and English texts.

## For developers

The page is maintained in a Claude conversation. Each update is published there and then pushed here.

| Path | What it is |
|---|---|
| `index.html` | The page (the same page published on claude.ai, wrapped as a home-screen app) |
| `p/*.json` | The text of each parsha: Hebrew, Targum, English and Rashi, loaded as needed |
| `g/*.json` | The Targum glossary for each parsha, loaded when you first tap a word |
| `manifest.webmanifest`, `sw.js`, `icons/` | Home-screen app settings, offline support and icons |
| `DECISIONS.md` | Every compromise and decision made in aligning and presenting the texts, and how the glossary works |
| `build/` | The scripts and hand-set fixes that produce the page (`build_page.py`, `align.py`, `fixes.py`, `ovr-*.json`, ...) and the glossary (`gloss_build.py`, with its dictionary and word lists in `build/gl/`); the Onkelos English: word-by-word matches in `build/eo-align/`, checked by `eo_check.py` and merged by `eo_merge.py` |
| `sources/` | The source texts as downloaded from Sefaria |
