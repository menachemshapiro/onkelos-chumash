import json,re,sys
E=json.load(open('../jastrow/jastrow-lookups.json'))['entries']; E.update(json.load(open('../jastrow/jastrow-lookups-2.json'))['entries'])
for r in sys.argv[1:]:
    e=E[r]; t=re.sub(r'\s+',' ',re.sub('<[^>]+>','',(e.get('language_reference') or '')+' '+' | '.join(s.get('definition','') for s in e['content'].get('senses',[]) if isinstance(s,dict))))
    print(r,e['headword'],'::',t[:220])
