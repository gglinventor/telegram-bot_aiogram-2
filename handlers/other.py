from aiogram import types, Dispatcher
from smart_piccer import pic, name_error, split_message, set_message, open_piccer, lower
from random import randint
from not_error import dp, bot
import time

#@dp.message_handler()
async def t_bot(message : types.Message):
    message.text = message.text.lower()
    count_ban = 0
    wo = split_message(message.text)
    if message.text in ('привет'):
        await message.answer('И тебе привет!')
    elif message.text in ('пока'):
        await message.answer('До скорой встречи!\See you again!')
    elif message.text in ('как дела', 'how are you', 'как дела?', 'how are you?'):
        answer = ['Нормально', 'Хорошо', 'Отлично', 'Прекрасно', 'Замечательно']
        await message.reply(answer[randint(0, 4)])
    elif set_message(split_message(message.text)).intersection(open_piccer('piccer.json')) != set():
        try:
            await bot.send_message(message.from_user.id, name_error())
        except:
            await message.answer(name_error())
        finally:
            print('\nbad word: ', wo, '\n')
            await message.delete()
            count_ban = 1
    elif count_ban != 1 and {pic(hrd, typ='all') for hrd in split_message(message.text)}.intersection(open_piccer('piccer.json')) != set() and {lower(rig) for rig in open_piccer('right.json')}.intersection(wo) == set():
        await message.reply('Внимание, подозрение на мат!')
    elif message.text == 'legendary film':
        await bot.send_message(message.from_user.id, 'https://www.youtube.com/watch?v=4enQp6CDiO8')
        time.sleep(4)
        await message.delete()
    elif message.text == 'happy new year':
        answer_2 = ['5', '4', '3', '2', '1', '0']
        for i in answer_2:
            await bot.send_message(message.from_user.id, i)
            time.sleep(0.5)
        await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAELEcNlkEijJt85t7ATZ20lbzcSQMlcKgACaR4AAh3tYUkpdZKPeRAC_jQE')
        await message.delete()

def check_handlers_other(dp : Dispatcher):
    dp.register_message_handler(t_bot)