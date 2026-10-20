"""Clause-by-clause re-split of pesukim whose English carries a long bracketed Onkelos rendering.
Each entry gives the English lines explicitly ({{...}} = bracketed Onkelos, shown highlighted),
optional Targum anchors 't' (first words of lines 2..n) and optional Hebrew word counts 'hw'.
A check makes sure the English words are exactly the original's (only their order changes)."""
import re, collections

NIQ = re.compile(r'[֑-ׇ]')

def norm(w): return re.sub(r'[^\wא-ת]', '', NIQ.sub('', re.sub(r'<[^>]+>', '', w))).lower()
def words(s): return [x for x in (norm(w) for w in re.sub(r'<[^>]+>', ' ', s).replace('[', ' ').replace(']', ' ').split()) if x]

def balance(parts, tag='b'):
    o, c = f'<{tag}>', f'</{tag}>'
    res, carry = [], False
    for p in parts:
        if carry: p = o + p
        carry = p.count(o) > p.count(c)
        if carry: p = p + c
        res.append(p)
    return res

def anchors(src, spec, key):
    toks = src.split(); nt = [norm(x) for x in toks]; cuts = [0]
    for a in spec:
        aw = [norm(x) for x in a.split()]
        pos = next((i for i in range(cuts[-1] + 1, len(toks)) if nt[i:i + len(aw)] == aw), None)
        if pos is None: raise SystemExit(f'REORDER ANCHOR MISS {key} {a}')
        cuts.append(pos)
    cuts.append(len(toks))
    return balance([' '.join(toks[a:b]) for a, b in zip(cuts, cuts[1:])])

def render(piece, orig):
    piece = re.sub(r'\{\{(.*?)\}\}', lambda m: '[<b>' + m.group(1) + '</b>]', piece)
    # plain [x] keeps the original's highlighting for x
    return re.sub(r'(?<![<\w])\[([^\[\]<]+)\](?!</b>)', lambda m: ('[<b>' + m.group(1) + '</b>]') if ('[<b>' + m.group(1) + '</b>]') in orig else m.group(0), piece)

R = {
'haazinu': {
 '32:12': {'e': ['Adonoy conducted them alone, {{Hashem alone will, in the future, place them in the world that He will renew}}',
                 'without [opposition by] alien gods. {{and no idol worship will exist before Him.}}']},
 '32:13': {'t': ['ואוכלנון', 'ויהב', 'ונכסי'],
           'e': ['He shall transport them over the summit of the earth {{He placed them in the strong places of the land,}}',
                 'where they will consume the produce of the fields; {{and He fed them the spoils of their enemies,}}',
                 'and He shall nurture them with honey of bedrock {{He gave them the spoils of the lords of cities,}}',
                 'and oil of staunchest rock mass. {{and the wealth of dwellers of fortified cities.}}']},
 '32:14': {'e': ['Butter-fat of cattle and milk of sheep with the fat of lambs, and rams native to Bashan and goats, {{He gave them the spoils of their kings and rulers with the wealth of their great and powerful, the people of their lands and their estates}}',
                 'with the fat of wheat kidneys, {{with the spoils of their armies and camps.}}',
                 'and the wine-flavored blood of the grapes will you drink. {{The blood of their heroes was spilled like water.}}']},
 '32:15': {'t': ['אצלח', 'ושבק', 'וארגז'],
           'e': ['Yeshurun grew fat and rebelled, {{Yisroel grew fat and rebelled.}}',
                 'you grew fat, you have become thick, and are covered with fat; {{He was very successful and wealthy}}',
                 'he forsook the God who made him, {{and forsook the service of the God Who made him,}}',
                 'he insulted the Rock of his salvation. {{and provoked the Almighty Who redeemed him.}}']},
 '32:19': {'t': ['מדארגיזו'],
           'e': ['Adonoy saw and was angered, {{It was apparent before Hashem, and His anger was kindled}}',
                 'by the spite of His sons and His daughters. {{by the provocations of sons and daughters before Him.}}']},
 '32:22': {'e': ['For a fire shall blaze in My anger, {{For a wind as strong as fire has gone out from before Me in anger,}}',
                 'that will burn till the lowest grave; {{which will destroy to the depths of the earth.}}',
                 'it shall consume the land and its produce, {{It will annihilate the land and its produce,}}',
                 'and enflame the bases of mountains. {{and destroy up to the edges of the mountains.}}']},
 '32:32': {'t': ['ולקותהון', 'מחתהון', 'ותשלמת'],
           'e': ['For their grapevine is of the grapevine [as the calamity of the nation] of Sedom',
                 'and from the fields [the calamity and deficiency as the nation] of Amorah;',
                 'their grapes are grapes of bitter herbs. {{You hit them as bad as the heads of serpents,}}',
                 'clusters galling to them. {{and the retribution for their deeds will be as bitter.}}']},
 '32:34': {'t': ['גניזין'],
           'e': ['Is this not sequestered with Me, {{Are not all of their deeds revealed before Me,}}',
                 'sealed in My treasuries. {{secreted away in my treasuries for the judgment day?}}']},
 '32:36': {'t': ['ופרענות', 'ארי', 'יהון'],
           'e': ['When Adonoy administers justice against His people {{When Hashem will decide the judgment of His people,}}',
                 'and He will reconsider about His servants; {{and the cruelty to His just servants will be revenged;}}',
                 'when He sees the power surging, {{then it will be apparent before Him that when the clout of their enemies will grow stronger,}}',
                 'and none are structured or fortified. {{they will be carried away and lost.}}']},
 '32:41': {'t': ['ותתקף', 'אתב', 'ולבעלי'],
           'e': ['If I whet My saber to a gleam, {{When My sword shall be revealed as a twofold lightning from one end of the heavens to the other,}}',
                 'and hold judgement in My grasp. {{My hand will hold fast to judgment}}',
                 'I shall wreak vengeance on My foes {{and I will visit calamity upon My enemies,}}',
                 'and My spiters will I pay. {{and I will repay my adversaries.}}']},
},
'vezot': {
 '33:2': {'t': ['אתחזי', 'ועמיה', 'כתב'],
          'e': ['He said: ‘‘Adonoy came [was revealed] from Sinai, [His glory] radiated forth to them from Seir,',
                'appeared [to us in His might] from Mount Paran',
                'He came with part of the sacred myriads;',
                'from [the writing of] His right [hand] — [from the midst of] the flaming [flame He gave the] Torah law [to us].']},
 '33:3': {'t': ['כל קדישוהי', 'ואנון', 'נטלין'],
          'e': ['He also cherished the nations — {{He even loved the tribes,}}',
                'all of their sacred ones are in Your keeping; {{the holy ones of the house of Israel, He mightily led them out of Egypt,}}',
                'for they were gathered in at Your feet {{and they are conducted under the "“cloud,”}}',
                'and accepted the burden of Your word. {{led by Your word.}}']},
 '33:6': {'e': ['May Reuvein live and let him not die, {{May Reuvein live forever, and a second death he shall not die.}}',
                'and may his constituency be counted. {{His children will receive their inheritance according to their numbers.}}']},
 '33:7': {'t': ['קבל', 'ולעמיה', 'ידוהי', 'וסעיד'],
          'e': ['Now this for Yehudah and he said, {{And this is for Yehudah, and he said:}}',
                '‘‘Adonoy, hear the voice of Yehudah, {{Accept, Hashem, the prayers of Yehudah when he goes out to wage war,}}',
                'and bring him to his people; {{and return his nation in peace.}}',
                'May his hands fight his battles {{Let his hand bring calamity upon his enemies,}}',
                'and may You provide assistance against his enemies.’’ {{and be for him a help against his enemies.}}']},
 '33:9': {'t': ['ואפי', 'ובנוהי', 'ארי', 'וקימך'],
          'e': ['He who said of his father and his mother, ‘I did not see them,‘ {{On his father and his mother he showed no mercy if they were (found) guilty by law,}}',
                'and his brothers he did not recognize {{nor did he "“recognize” his brothers}}',
                'and his sons he did not know; {{or children,}}',
                'for they observed Your command {{for they guarded the charge of Your word}}',
                'and kept Your covenant. {{and did not alter Your covenant.}}']},
 '33:17': {'e': ['His firstborn ox, glory to him, and re’em’s horns are his horns, {{The greatness of his children will be his beauty, and the mighty things [miracles] done for him from before the Almighty and Most High,}}',
                 'with which he will gore together peoples to the ends of the earth; {{with his might he will slay nations as one to the ends of the earth.}}',
                 'and they are Ephraim’s myriads, {{They are the myriads of the house of Ephraim}}',
                 'and they are Menasheh’s thousands.’’ {{and they are the thousands of the house of Menasheh.}}']},
 '33:18': {'t': ['חדי', 'ויששכר'],
           'e': ['And regarding Zevulun he said,',
                 '‘‘Rejoice Zevulun at your departure; {{Rejoice Zevulun when you go out to wage war on your enemies,}}',
                 'and Yissachar in your tents {{and Yissachar when you go to calculate the times of the Festivals in Yerushalayim.}}.']},
 '33:26': {'e': ['[There is no] God is incomparable — Yeshurun {{as the God of Yisrael}}',
                 'He who straddles the firmament in your aid {{Whose Shechinah in the heaven is your help}};',
                 'and, in His pride, [might is in] the high heavens.']},
},
'balak': {
 '23:19': {'e': ['God is not like man that He should act falsely, {{God’s word is not as that of man who speaks with deceit.}}',
                 'nor is He mortal that He should change His mind. {{Nor is it as that of mankind who decree and then change their mind}}',
                 'Would He say and not do it? {{He says and does,}}',
                 'Or speak and not fulfill it {{and His word endures}}?']},
},
'behaalotecha': {
 '12:12': {'e': ['Please let her not be like the dead [separated from among us for she is our sister];',
                 'That, since he came from his mother’s womb, {{pray now for this dead flesh which is in her,}}',
                 'it would be as half of his own flesh was consumed {{so she will be healed}}.”']},
},
'beshalach': {
 '15:11': {'e': ['Who is like You among the mighty, Adonoy! {{There is none besides You, for You are God, Adonoy!}}',
                 'Who is like You, adorned in holiness, {{There is none besides You, O God, You are adorned in holiness,}}',
                 'Awesome in praise, doing wonders? {{Awesome in praise, doing wonders!}}']},
 '17:16': {'e': ['He said, “The hand is on God’s throne, {{with an oath, this saying from before the Awesome one, whose Shechina is upon His glorious throne,}}',
                 'Adonoy will be at war with Amaleik {{that in the future a war will be waged before God against the house of Amaleik}}',
                 'for all generations.” {{to destroy them for generations forever.}}']},
},
'lechlecha': {
 '13:16': {'e': ['I will make your descendants [numerous] as the dust of the earth;',
                 'so that if a man can count the dust of the earth, {{just as it is impossible for a man to count the dust of the earth,}}',
                 'then your descendants too will be countable {{so too your descendants will not be countable}}.']},
 '14:17': {'e': ['The King of Sedom went out to meet him', 'after his return from defeating Kedorlaomer',
                 'and the kings that were with him,', 'to the Valley of Shaveh {{to the barren plain,}}',
                 'which is the King’s Valley {{which is the place of the racetrack of the king}}.']},
},
'noach': {
 '11:5': {'e': ['Adonoy descended {{Adonoy became revealed}}',
                'to see {{in order to punish them because of the building of}} the city and the tower',
                'that the sons of man built.']},
},
'vaera': {
 '8:22': {'e': ['Moshe said, “It would not be proper to do so.',
                'For that which is abominable [sacred] to Egypt {{the animal that the Egyptians worship}}',
                'we intend to sacrifice to {{we are taking to sacrifice before}} Adonoy, our God.',
                'Could we sacrifice the abomination of the Egyptians before their eyes and not have them stone us? {{Behold, we will sacrifice the animal that the Egyptians worship, and they will see. Will they not want to stone us?}}']},
},
'vayechi': {
 '49:9': {'hw': [3, 3, 3, 3], 't': ['ארי', 'ינוח', 'וכליתא'],
          'e': ['Yehudah is like a young lion. {{He will be a ruler at the beginning, and at the end, a king will be anointed from the house of Yehudah.}}',
                'You have risen above plunder my son. {{For from the judgment of death, my son, you removed yourself.}}',
                'He crouches, rests like a lion, {{He will rest and dwell in strength like a lion.}}',
                'like an awesome lion, who will rouse him? {{there is no kingdom that can make him tremble.}}']},
 '49:11': {'hw': [4, 3, 3, 3], 't': ['יהון', 'יהי', 'כסותיה'],
           'e': ['He loads his young donkey with grapes of a vine, {{He will bring Israel from all around to his city, the nation who will build his Temple.}}',
                 'and his she-donkey’s foal with a vine-branch. {{The righteous will congregate around the Moshiach, and those who engage in Torah will study with him.}}',
                 'He washes his clothes in wine, {{May his garments be of fine purple cloth,}}',
                 'and his cloak in the blood of grapes {{and his clothes of fine wool colored in scarlet and other colors}}.']},
 '49:17': {'hw': [3, 2, 2, 3], 't': ['וכפתנא', 'יקטל', 'וימגר'],
           'e': ['Dan will be a serpent on the road, {{The man that will be chosen and will arise from the house of Dan — his terror will fall upon the peoples, and his smiting will be strong against the Pelishtim. Like a viper he will lie on the way,}}',
                 'a viper on the path {{and like an old snake he will ambush on the path}},',
                 'that bites the horse’s heel {{He will kill the mighty of the camp of the Plishtim / the horsemen with the infantry / He will uproot the horses and chariots}}',
                 'so that the rider falls backward {{and he will cause their riders to fall backward}}.']},
},
'vayera': {
 '20:16': {'e': ['To Sarah, he said, Behold I have given to your brother a thousand pieces [shekalim] of silver.',
                 'It will be for you a [compensational] eye covering {{It will be for you a garment of honor, in return for my having sent for you, and taken you, and seeing you}}',
                 'for all who are with you, {{and all that is with you.}}',
                 'that you may face every one. {{And regarding everything that you said, you were just.}}']},
 '21:22': {'e': ['It was at this time,', 'Avimelech and Pichol, his general', 'spoke to Avraham, saying,',
                 'Elohim is with you {{the Word of Elohim is your support}}',
                 'in all that you do {{in all that you do}}.']},
 '22:14': {'e': ['Avraham called the name of that place, Adonoy will see; {{Avraham worshiped and prayed there in that place, and he said before Adonoy, “Here will generations worship”.}}',
                 'as it is said [to] this day, {{Therefore, as it is said [to] this day,}}',
                 'On Adonoy’s mountain, He will be seen. {{“On this mountain Avraham worshiped before Adonoy”.}}']},
},
'vayetzei': {
 '31:39': {'e': ['I never brought you a mutilated animal.',
                 'I will take the blame for it. {{for that which was missing from the total.}}',
                 'You demanded compensation from my hand {{You demanded compensation from me}}',
                 'whether [an animal] was stolen from me by day {{I guarded by day}}',
                 'or whether it was stolen from me by night. {{and I guarded by night.}}']},
},
}

def apply(pid, c, v, h, t, e):
    o = R.get(pid, {}).get(f'{c}:{v}')
    if not o: return h, t, e
    key = f'{pid} {c}:{v}'
    if 'hw' in o:
        ws = ' '.join(h).split(' ')
        assert sum(o['hw']) == len(ws), (key, len(ws))
        k, nh = 0, []
        for n in o['hw']: nh.append(' '.join(ws[k:k + n])); k += n
        h = nh
    if 't' in o: t = anchors(' '.join(t), o['t'], key)
    orig = ' '.join(e)
    ne = [render(p, orig) for p in o['e']]
    a, b = collections.Counter(words(orig)), collections.Counter(words(' '.join(ne)))
    if a != b: raise SystemExit(f'REORDER WORDS {key} missing={list((a - b).elements())} extra={list((b - a).elements())}')
    for nm, arr in (('t', t), ('e', ne)):
        if len(arr) != len(h): raise SystemExit(f'REORDER COUNT {key} {nm} {len(arr)} vs {len(h)}')
    return h, t, ne
