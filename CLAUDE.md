# Project rules

## Every update to the live site
Whenever a change goes to `main` (that is what GitHub Pages serves), also:

1. **Update the version number in the help popup (?).** It is the line `<p class="help-ver" id="app-ver">Version YYYY.MM.DD</p>` at the end of the help text. Use the date of the update (Israel time). For a second update on the same day, add `.2`, `.3`, … (e.g. `2026.11.05.2`).
2. Change it in both `build/page-template.html` and `index.html`. `index.html` is `page-template.html` wrapped by `build/make_site.py`.
3. **Change `VERSION` in `sw.js`**, so installed home-screen copies fetch the new page.
4. Add a line to `TODO.md` (Done) and, for decisions, `DECISIONS.md`.

## Reports
Reports from the GitHub copy are GitHub issues on this repository (label `report`, with a hidden `<!-- report {...} -->` line naming the pasuk). "Check the reports" means: read the open issues, fix what they describe, then close each one with a comment saying what changed.
