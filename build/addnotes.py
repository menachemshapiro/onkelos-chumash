"""addnotes.py NOTESFILE : add notes to eo-align files. Each line: pid<TAB>c:v<TAB>clause#<TAB>note
The note goes after the clause's M line and any notes already there."""
import sys, collections
todo = collections.defaultdict(list)
for l in open(sys.argv[1], encoding='utf8'):
    if not l.strip() or l.startswith('#'): continue
    pid, cv, k, note = l.rstrip('\n').split('\t'); todo[pid].append((cv, int(k), note))
for pid, items in todo.items():
    p = f'eo-align/{pid}.txt'; L = open(p, encoding='utf8').read().split('\n')
    for cv, k, note in items:
        i = L.index('@ ' + cv); n = 0; j = i + 1
        while True:
            if L[j].startswith('E: ') or L[j] == '= same': n += 1
            if n == k: break
            j += 1
        assert L[j].startswith('E: '), (pid, cv, k, L[j])
        e = L[j]; j += 1
        while j < len(L) and (L[j].startswith(('M: ', '+', '! '))): j += 1
        L.insert(j, '! ' + note)
        print(pid, cv, k, '|', e[3:][:90], '\n    !', note)
    open(p, 'w', encoding='utf8').write('\n'.join(L))
