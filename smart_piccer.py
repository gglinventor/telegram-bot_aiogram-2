import string, json
def pic(i, typ):
    global name
    w = set()
    w.add(i)
    i_2 = list(i)
    if len(i_2) in (1, 2):
        return i
    elif open_piccer('good_http.json').intersection(w) != set():
        return i
    #print('\n', '\n','\n','\n', w)
    #with open('piccer.txt', encoding='utf-8') as r:
    for r_2 in open_piccer('piccer.json'):
        r_2 = lower(r_2)
        if r_2 != '':
            count_intersection = 0
            count_u = 0
            for y in r_2:
                if y == i_2[count_u]:
                    count_intersection += 1
                if len(i) > count_u + 1:
                    count_u += 1
                else:
                    break
            if count_intersection / len(i) * 100 >= 60:
                #print(r_2, i)
                #print('suspicion of swearing: ', w)
                #print(count_intersection, len(i), '%', count_intersection / len(i) * 100)
                if typ == 'all' and len(r_2) == len(i_2):
                    i = r_2
                name = 'Обзываться не хорошо!'
                break
            elif r_2 in ('https://', 'http://') and count_intersection / 7 * 100 >= 100:
                #print(r_2, i)
                #print('suspicion of swearing: ', w)
                #print(count_intersection, len(i), '%', count_intersection / len(i) * 100)
                i = 'плохой'
                name = 'Ссылки запрещены'
                break                 
    return i

name = ''

def name_error():
    global name
    return name

def split_message(message):
    return {mes for mes in message.split(' ')}

def set_message(message):
    return {pic(i, typ='http').lower().translate(str.maketrans('', '', string.punctuation + '0123456789')) for i in message}

def open_piccer(file):
    return set(json.load(open(file)))

def lower(word):
    return word.lower()

async def menu_price_piccer(message):
    if {i for i in message.text}.intersection({'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ','}) == {i for i in message.text}:
        data = round(float(message.text.replace(',', '.')), 2)
    else:
        data = 'Не установлена'
        #print(message.text, 'Type: ', type(message.text))
        await message.reply('Неправильный ввод, значение не установлено!\nЦену следует вводить следующим образом: 549.99 - тоесть ТОЛЬКО ЧИСЛО')
    return data