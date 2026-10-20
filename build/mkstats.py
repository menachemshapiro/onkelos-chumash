# mkstats.py: regenerate ../glossary-stats.html from gl-stats.json (one table per book)
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
S = json.load(open('gl-stats.json'))
NAMES = {'bereishit':('בראשית','Bereishit'),'noach':('נח','Noach'),'lechlecha':('לך לך','Lech Lecha'),'vayera':('וירא','Vayera'),
 'chayeisarah':('חיי שרה','Chayei Sarah'),'toldot':('תולדות','Toldot'),'vayetzei':('ויצא','Vayetzei'),'vayishlach':('וישלח','Vayishlach'),
 'vayeshev':('וישב','Vayeshev'),'miketz':('מקץ','Miketz'),'vayigash':('ויגש','Vayigash'),'vayechi':('ויחי','Vayechi'),
 'shemot':('שמות','Shemot'),'vaera':('וארא','Vaera'),'bo':('בא','Bo'),'beshalach':('בשלח','Beshalach'),'yitro':('יתרו','Yitro'),
 'mishpatim':('משפטים','Mishpatim'),'terumah':('תרומה','Terumah'),'tetzaveh':('תצוה','Tetzaveh'),'kitisa':('כי תשא','Ki Tisa'),
 'vayakhel':('ויקהל','Vayakhel'),'pekudei':('פקודי','Pekudei'),
 'vayikra':('ויקרא','Vayikra'),'tzav':('צו','Tzav'),'shemini':('שמיני','Shemini'),'tazria':('תזריע','Tazria'),'metzora':('מצורע','Metzora'),
 'achareimot':('אחרי מות','Acharei Mot'),'kedoshim':('קדושים','Kedoshim'),'emor':('אמור','Emor'),'behar':('בהר','Behar'),'bechukotai':('בחוקותי','Bechukotai'),
 'bamidbar':('במדבר','Bamidbar'),'naso':('נשא','Naso'),'behaalotecha':('בהעלותך','Behaalotecha'),'shelach':('שלח','Shelach'),'korach':('קרח','Korach'),
 'chukat':('חקת','Chukat'),'balak':('בלק','Balak'),'pinchas':('פינחס','Pinchas'),'matot':('מטות','Matot'),'masei':('מסעי','Masei'),
 'devarim':('דברים','Devarim'),'vaetchanan':('ואתחנן','Vaetchanan'),'eikev':('עקב','Eikev'),'reeh':('ראה','Re\'eh'),'shoftim':('שופטים','Shoftim'),
 'kiteitzei':('כי תצא','Ki Teitzei'),'kitavo':('כי תבוא','Ki Tavo'),'nitzavim':('נצבים','Nitzavim'),'vayeilech':('וילך','Vayeilech'),'haazinu':('האזינו','Haazinu'),'vezot':('וזאת הברכה','Vezot Haberachah')}
BOOKS = [('Bereishit','בראשית',list(NAMES)[:12]),('Shemot','שמות',list(NAMES)[12:23]),('Vayikra','ויקרא',list(NAMES)[23:33]),('Bamidbar','במדבר',list(NAMES)[33:43]),('Devarim','דברים',list(NAMES)[43:])]
f = lambda n: f'{n:,}'
cal_total = len(json.load(open('cal-log.json'))['calls'])
out = [open('stats-head.html').read().rstrip(), '<main>', '<h1>Targum Onkelos glossary · counts by aliyah</h1>',
 '<p>Counts for each aliyah, in reading order. “New” means the word or root has not appeared in any earlier aliyah (Shemot is compared against all of Bereishit too).</p>']
allw = sum(r['words'] for r in S)
out.append(f'<div class="sum"><span><b>{f(allw)}</b> Targum words</span><span><b>{f(sum(r["forms_new"] for r in S))}</b> different spellings</span>'
 f'<span><b>{f(sum(r["roots_new"] for r in S))}</b> roots</span><span><b>{cal_total}</b> CAL lookups since the safeguards</span></div>')
out.append('''<div class="key">
<span><b>Spellings</b>: different written forms in the aliyah (וַאֲמַר and אֲמַר count as two). <b>Seen</b>: already appeared earlier. <b>New</b>: first time.</span>
<span><b>Roots</b>: different roots in the aliyah. Names and small words with no root (יָת, דִּי, עַל) are not counted.</span>
<span><b>CAL</b>: pages fetched from the Comprehensive Aramaic Lexicon while checking that aliyah.</span>
</div>''')
TH = '<thead><tr><th scope="col">Aliyah</th><th scope="col">Words</th><th scope="col">Spellings</th><th scope="col">Seen</th><th scope="col">New</th><th scope="col">Roots</th><th scope="col">Seen</th><th scope="col">New</th><th scope="col">CAL</th></tr></thead>'
for en, he, pids in BOOKS:
    rows = [r for r in S if r['parsha'] in pids]
    if not rows: continue
    out.append(f'<h2 style="font:700 1.4rem/1.2 var(--display);margin:8px 0 0;color:var(--accent)"><span lang="he">ספר {he}</span> · {en}</h2>')
    out.append(f'<div class="sum"><span><b>{f(sum(r["words"] for r in rows))}</b> words</span><span><b>{f(sum(r["forms_new"] for r in rows))}</b> new spellings</span><span><b>{f(sum(r["roots_new"] for r in rows))}</b> new roots</span><span><b>{sum(r["cal"] for r in rows)}</b> CAL</span></div>')
    out.append('<div class="wrap"><table>'); out.append(TH); out.append('<tbody>')
    for p in pids:
        pr = [r for r in rows if r['parsha'] == p]
        if not pr: continue
        h, e = NAMES[p]
        out.append(f'<tr class="ph"><th colspan="9" scope="rowgroup"><span class="he">{h}</span> {e}<span class="phs">{f(sum(r["words"] for r in pr))} words · {f(sum(r["forms_new"] for r in pr))} new spellings · {sum(r["roots_new"] for r in pr)} new roots · {sum(r["cal"] for r in pr)} CAL</span></th></tr>')
        for r in pr:
            cal = '≈47*' if r['aliyah'] == 'bereishit-1' else (str(r['cal']) if r['cal'] else '·')
            rg = f"{r['from'][0]}:{r['from'][1]}–{r['to'][0]}:{r['to'][1]}"
            out.append(f"<tr><td class='al'><span class='he'>{r['name']}</span><span class='rg'>{rg}</span></td><td>{r['words']}</td><td>{r['forms']}</td><td>{r['forms_repeat']}</td><td class='nw'>{r['forms_new']}</td><td>{r['roots']}</td><td>{r['roots_repeat']}</td><td class='nw'>{r['roots_new']}</td><td>{cal}</td></tr>")
    out.append('</tbody></table></div>')
out.append('<p class="note">* About 47 lookups for the first aliyah were made before the safeguards and were not logged, so that figure is an estimate. Bereishit שני and שלישי include 8 lookups that repeated earlier checks after a restart.</p>')
out.append('</main>')
open('../glossary-stats.html', 'w').write('\n'.join(out) + '\n')
print('ok', len(S), 'aliyot')
