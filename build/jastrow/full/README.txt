Jastrow Dictionary - Sefaria-Data copy (last version before deletion)

Source: github.com/Sefaria/Sefaria-Data, the parent of commit 2151151c70752bd6853658a20f2c86061f0462b7
("Delete dicts"), i.e. the last commit that still had the dictionary files. Text: Marcus Jastrow,
A Dictionary of the Targumim, the Talmud Babli and Yerushalmi, and the Midrashic Literature (London, Luzac, 1903).

Contents
  Jastrow-full-2017.xml    the whole dictionary in one XML file (32,512 entries); the copy our site's build reads
  Jastrow-full.xml         a second full XML in the repository; nearly identical (small differences in page-break markup)
  sefaria_dictionary.dtd   the XML schema both files follow
  separate/                the same dictionary split into one XML file per letter (01-aleph ... 22-tav)
  html/                    one HTML file per letter (A-V, Sefaria's entry-id letters), with jastrow.css
  code/                    Sefaria's scripts that parsed and loaded the XML into their database

Entry ids (A00001, B00002 ...) are the same ids Sefaria's site and API use today.
