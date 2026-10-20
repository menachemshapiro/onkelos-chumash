# alltab.py : every token in the Torah with its gloss -> all-gloss.tsv (pid c:v token how lexkey here pre)
import runpy, sys, unicodedata as u
sys.argv = ['gloss_build.py', 'todo', 'none']
G = runpy.run_path('gloss_build.py', run_name='bt')
with open('all-gloss.tsv', 'w') as f:
    for a in G['ALIYOT']:
        for c, v, toks in a[2]:
            for i, t in enumerate(toks):
                e, how = G['lookup'](t, c, v, a[0], toks[i - 1] if i else None)
                if not e: f.write(f'{a[0]}\t{c}:{v}\t{u.normalize("NFC",t)}\tMISSING\t\t\t\n'); continue
                pre = '+'.join(p[1] for p in e.get('pre', []))
                f.write(f'{a[0]}\t{c}:{v}\t{u.normalize("NFC",t)}\t{how}\t{e["l"]}\t{e.get("here","")}\t{pre}\t{u.normalize("NFC",e.get("derived",""))}\t{e.get("f","")}\n')
