"""Log of every request made to the CAL website (cal.huc.edu), plus the saved answers.
usage: python3 callog.py add <aliyah-key> <form> <url> <answer>   (records one request)
       python3 callog.py get <form>                                 (prints a saved answer, if any)
       python3 callog.py count                                      (requests per aliyah)"""
import json, sys, time, os
F = os.path.join(os.path.dirname(__file__), 'cal-log.json')
d = json.load(open(F)) if os.path.exists(F) else {'calls': [], 'answers': {}}
cmd = sys.argv[1]
if cmd == 'add':
    a, form, url, ans = sys.argv[2:6]
    d['calls'].append({'aliyah': a, 'form': form, 'url': url, 'time': time.strftime('%Y-%m-%d %H:%M:%S')})
    d['answers'][form] = ans
    json.dump(d, open(F, 'w'), ensure_ascii=False, indent=0)
elif cmd == 'get':
    print(d['answers'].get(sys.argv[2], ''))
elif cmd == 'count':
    from collections import Counter
    for k, n in Counter(c['aliyah'] for c in d['calls']).items(): print(k, n)
    print('total', len(d['calls']))
