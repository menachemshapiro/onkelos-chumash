# vtxt.py pid c:v ... : print Onkelos + English for verses
import json,sys,re
for a in sys.argv[1:]:
    p,cv=a.split('/'); c,v=cv.split(':')
    for x in json.load(open(f'../p/{p}.json'))['V']:
        if str(x['c'])==c and str(x['v'])==v: print(p,cv,re.sub('<[^>]+>','',' '.join(x['t'])),'||',re.sub('<[^>]+>','',' '.join(x['e'])))
