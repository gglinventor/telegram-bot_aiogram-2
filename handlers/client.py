from aiogram import types, Dispatcher
from not_error import dp, bot
from keyboard import key_client
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from data_base import sqlite_data

from datetime import datetime

inl_key_client = [InlineKeyboardButton(text=f'{i}', callback_data=f'like_{i}') for i in range(1, 6)]

inl_key_client_all = InlineKeyboardMarkup(row_width=5).row(inl_key_client[0], inl_key_client[1], inl_key_client[2], inl_key_client[3], inl_key_client[-1])

names_help = ['Все команды', 'Ошибка', 'Тех. поддержка']

names_question = ['Время работы', 'Расположение', 'Персонал']

names_menu = ['Пицца', 'Закуски', 'Напитки']

names_feedback = ['Оставить оценку', 'Рейтинг', 'Отзывы']

help_answer = ['/start - бот выводит клавиатуру для пользователя и здоровается с ним\n/Частые_вопросы - частые вопросы заведения\n/Тех_поддержка (/help)- указания, если возникли трудности при работе с ботом\n/Меню (/menu)- показывает какие товары производит пиццерия, их цену, описание и так далее\n/Отзывы - команда, чтобы оставить оценку, посмотреть рейтинг и прочитать отзывы пиццерии\n/Поделиться номером - нажав на команду, вы оставите свой номер для связи продавца с вами\n/Отправить местоположение - отправить местоположение для возможной доставки пиццы',
               '1)НЕВНИМАТЕЛЬНОСТЬ\nПрочитайте все сообщения в основной группе https://t.me/+B-z9OTeNyU0zMjcy возможно вы не заметили важных объявлений касающихся бота, например: "Временное отключение некоторых функций" и другие, или вы некорректно следовали указаниям бота. Также проверьте у себя подключение к интернету, это очень частая проблема у пользователей!\n\n2)НЕМНОГО ТЕРПЕНИЯ\nПодождите некотрое время, возможно бот был нагружен работой и ещё не успел ответить, возможно сервера телеграма зависли и не отвечают на запрос, но суть всего этого в том, что надо немного подождать или ещё раз отправить запрос боту.',
               'Если указания в кнопке "Ошибка" вам не помогли, то обратитесь за помощью к администратору https://t.me/GGL_Inventor но обращайтесь за помощью, если действительно трудная ситуация. Администратор - человек и ответит не сразу!']

error_answer = ['Общение с ботом в ЛС, напишите ему: \nhttps://t.me/Pizza_inventor_bot\n\nP.s.Бот не виноват, что не может вам написать, такие правила Телеграма :(',
                'Поторите запрос или обратитесь в Тех. поддержку, через комаду /help']

question_answer = ['Время работы по будням:\nс 8:00 до 22:00\n\nВремя работы по выходным:\n с 7:00 до 00:00', 'Пиццерия "БЫСТРО И ВКУСНО" располагается в России, в Краснодарском крае, город Краснодар, \nа дальше сам ищи, гугл и яндекс карты в помощь :)', 'Так как Пиццерия "БЫСТРО И ВКУСНО" является Индивидуальным Предпринемателем (ИП),\nвесь персонал состоит из Василия Васильевича Литвинова']

def command_client_error(first_name, id, e, function=None):
    now_time = datetime.now()
    print(f'\nException:\nID: {first_name} ({id}) {now_time.year}-{now_time.month}-{now_time.day} {now_time.hour}:{now_time.minute}:{now_time.second}\n{function}: ', e, '\n')
 
#####START#####

#@dp.message_handler(commands=['start', 'Start'])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Пиццерия "БЫСТРО И ВКУСНО" приветствует вас!\nПриятного аппетита!', reply_markup=key_client)
        await message.delete()
    except Exception:
        await message.answer(error_answer[0])

#####HELP#####

#@dp.message_handler(commands=['help', 'Help'])
#@dp.message_handler(Text(equals='тех поддержка'))
async def command_help(message: types.Message):
    try:
        def list_keyboard_help():
            return [InlineKeyboardButton(text=names_help[i], callback_data=f'help_{i}') for i in range(3)]
        e = list_keyboard_help()
        await bot.send_message(message.from_user.id, text='У вас возникли трудности? Следующий набор кнопок постарается решить вашу проблему!\n\n1)Если возникли трудности с пониманием команд, нажмите на кнопку "Все команды"\n\n2)Если какая-то команда не работает, нажмите на кнопку "Ошибка"\n\n3)Если ничего не поможет, обратитесь в поддержку, нажав на кнопку "Тех. поддержка"', reply_markup=InlineKeyboardMarkup(row_width=3).row(e[0], e[1], e[2]))
        await message.delete()
    except Exception:
        await message.answer(error_answer[0])

#@dp.callback_query_handler(lambda z: z.data and z.data.startswith('help_'))
async def command_callback_help(callback: types.CallbackQuery):
    try:
        typ = callback.data.replace('help_', '')
        await callback.message.answer(help_answer[int(typ)])
        await callback.answer()
    except Exception as e:
        command_client_error(callback.from_user.first_name, callback.from_user.id, e, 'command_callback_help')
        await callback.answer('Поторите запрос или обратитесь в Тех. поддержку, через комаду /help', show_alert=True)

#####OFFEN_QUESTIONS#####
            
#@dp.message_handler(Text(equals='частые вопросы')) #commands=['Частые_вопросы', 'частые_вопросы']
async def command_question(message: types.Message):
    try:
        def list_keyboard_question():
            return [InlineKeyboardButton(text=names_question[i], callback_data=f'question_{i}') for i in range(3)]
        e_ques = list_keyboard_question()
        await bot.send_message(message.from_user.id, text='Часто задаваемые вопросы:', reply_markup=InlineKeyboardMarkup(row_width=3).row(e_ques[0], e_ques[1], e_ques[2]))
        await message.delete()
    except Exception as e:
        command_client_error(message.from_user.first_name, message.from_user.id, e, 'command_question')
        await message.answer(error_answer[1])

#@dp.callback_query_handler(lambda c: c.data and c.data.startswith('question_'))
async def command_calback_question(callback: types.CallbackQuery):
    try:
        typ_question = callback.data.replace('question_', '')
        await callback.message.answer(question_answer[int(typ_question)])
        await callback.answer()
    except Exception as e:
        command_client_error(callback.from_user.first_name, callback.from_user.id, e, 'command_callback_question')
        await callback.answer('Поторите запрос или обратитесь в Тех. поддержку, через комаду /help', show_alert=True) 

#####MENU#####

#@dp.message_handler(commands=['menu', 'Menu'])
#@dp.message_handler(Text(equals='меню'))
async def command_menu(message : types.Message):
    try:
        def list_keyboard_menu():
            return [InlineKeyboardButton(text=names_menu[i], callback_data=f'menu_{i+1}') for i in range(3)]
        e_menu = list_keyboard_menu()
        await bot.send_message(message.from_user.id, text='Выберите тип еды:', reply_markup=InlineKeyboardMarkup(row_width=3).add(e_menu[0]).row(e_menu[1], e_menu[2]))
        await message.delete()
    except Exception:
        await message.answer(error_answer[0])

#@dp.callback_query_handler(lambda a: a.data and a.data.startswith('menu_'))
async def command_callback_menu(callback: types.CallbackQuery):
    try:
        type_food = callback.data.replace('menu_', '')
        await sqlite_data.sql_menu(callback, type_food)
        await callback.answer()
    except Exception as e:
        command_client_error(callback.from_user.first_name, callback.from_user.id, e, 'command_callback_menu')
        await callback.answer(error_answer[1])

#####FEEDBACK##### 

#@dp.message_handler(Text(equals='отзывы')) #commands=['Отзывы', 'отзывы']
async def command_feedback(message: types.Message):
    try:
        def list_keyboard_feedback():
            return [InlineKeyboardButton(text=names_feedback[i], callback_data=f'feedback_{i}') for i in range(3)]
        e_back = list_keyboard_feedback()
        await bot.send_message(message.from_user.id, text='Выберите команду:', reply_markup=InlineKeyboardMarkup(row_width=3).row(e_back[0], e_back[1], e_back[2]))
        await message.delete()
    except Exception as e:
        command_client_error(message.from_user.first_name, message.from_user.id, e, 'command_feedback')
        await message.answer(error_answer[1])

#@dp.callback_query_handler(lambda b: b.data and b.data.startswith('feedback_'))
async def command_callback_feedback(callback: types.CallbackQuery):
    try:
        typ_back = callback.data.replace('feedback_', '')
        if typ_back == '0':
            await callback.message.answer('Как вы оцените нашу пиццерию?', reply_markup=inl_key_client_all)
        elif typ_back == '1':
            res = await sqlite_data.sql_table_2_read('result')
            await callback.message.answer(f'Рейтинг пиццерии: "БЫСТРО И ВКУСНО",\nсостовляет {round(res, 1)} из 5')
        elif typ_back == '2':
            await callback.message.answer('Прочитать отзывы можно в группе: https://t.me/+B-z9OTeNyU0zMjcy')
        await callback.answer()
    except Exception as e:
        command_client_error(callback.from_user.first_name, callback.from_user.id, e, 'command_callback_feedback')
        await callback.answer(error_answer[1])

#@dp.callback_query_handler(Text(startswith='like_'))
async def inline_command_survey(callback: types.CallbackQuery):
    try:
        result = int(callback.data.split('_')[1])
        survey_data = await sqlite_data.sql_table_2_read('user_id')
        if callback.from_user.id not in tuple(survey_data):
            print(callback.from_user.id, 'all == ', tuple(survey_data))
            await sqlite_data.sql_table_2_write(callback.from_user.id, callback.from_user.first_name, callback.from_user.username, result)
            await callback.answer('Спасибо за отзыв!', show_alert=True)
        else:
            await callback.answer('Вы уже проголосовали!!!', show_alert=True)
    except Exception as e:
        command_client_error(callback.from_user.first_name, callback.from_user.id, e, 'inline_command_survey')
        await callback.answer(error_answer[1])
        

def check_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'Start'])
    dp.register_message_handler(command_help, commands=['help', 'Help'])
    dp.register_message_handler(command_help, Text(equals='тех поддержка'))
    dp.register_callback_query_handler(command_callback_help, lambda z: z.data and z.data.startswith('help_'))
    dp.register_message_handler(command_question, Text(equals='частые вопросы'))
    dp.register_callback_query_handler(command_calback_question, lambda c: c.data and c.data.startswith('question_'))
    dp.register_message_handler(command_menu, commands=['menu', 'Menu'])
    dp.register_message_handler(command_menu, Text(equals='меню'))
    dp.register_callback_query_handler(command_callback_menu, lambda a: a.data and a.data.startswith('menu_'))
    dp.register_message_handler(command_feedback, Text(equals='отзывы'))
    dp.register_callback_query_handler(command_callback_feedback, lambda b: b.data and b.data.startswith('feedback_'))
    dp.register_callback_query_handler(inline_command_survey, Text(startswith='like_'))