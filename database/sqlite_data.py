import sqlite3 as sql
from not_error import bot, dp
from aiogram import types
#from Pizza_bot import base, cur

############DATABASE_TABLE_№1############

async def sql_start():
    global base, cur
    base = sql.connect('pizza_col.db')
    cur = base.cursor()
    if base:
        print('data base successful start')
    base.execute('CREATE TABLE IF NOT EXISTS menu(number PRIMARY KEY, img TEXT, name TEXT, info TEXT, price TEXT, valute TEXT, type_food TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS survey(user_id TEXT PRIMARY KEY, first_name TEXT, username TEXT, result INTEGER)')
    base.commit()

async def sql_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?, ?, ?, ?)', (len(cur.execute('SELECT * FROM menu').fetchall()),) + tuple(data.values()))
        base.commit()
        print('Append: ', tuple(data.values()))

async def sql_menu(callback, type_food):
    for ret in cur.execute('SELECT * FROM menu WHERE type_food == ?', (type_food,)).fetchall():
        await bot.send_photo(callback.from_user.id, (ret[1]), f'{ret[2]}\nОписание: {ret[3]}\nЦена: {ret[4]} {ret[5]}')

async def sql_read():
    return cur.execute('SELECT * FROM menu').fetchall()

async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()
    print('Delete: ', data)
    q = await sql_read()
    for i in q:
        if i[0] != q.index(i):
            cur.execute('UPDATE menu SET number == ? WHERE number == ?', (q.index(i), i[0])) # sql_replace_command(['number', 'number', q.index(i), i[0]])
    base.commit()

async def sql_replace_command(data):
    cur.execute(f'UPDATE menu SET {data[0]} == ? WHERE {data[1]} == ?', (data[2], int(data[3])))
    base.commit()
    print('Replace: ', data)
    

############DATABASE_TABLE_№2############

async def sql_table_2_write(user_id, first_name, username, result):
    cur.execute('INSERT INTO survey VALUES (?, ?, ?, ?)', (user_id, first_name, username, result))
    base.commit()
    
async def sql_table_2_read(column):
    res = cur.execute('SELECT * FROM survey').fetchall()
    if column in ('user_id'):
        return [int(i[0]) for i in res]
    elif 'result' in column:
        res = [i[3] for i in res]
        if res == []:
            res = 4.9
        else:
            i_2 = 0
            for i in res:
                i_2 += i
            res = i_2 / len(res)
            print(res)
        return res


        
