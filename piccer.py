import json

pic_txt = []

with open('right.txt', encoding='utf-8') as q:
    for i in q:
        d = i.lower().split('\n')[0]
        if d != '':
            pic_txt.append(d)

with open('right.json', 'w', encoding='utf-8') as w:
    json.dump(pic_txt, w)
