
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from not_error import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from data_base import sqlite_data
from keyboard import admin_key
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from smart_piccer import menu_price_piccer

ID = []
names = ['Фото', 'Название', 'Описание', 'Цена', 'Валюта', 'Тип']
names_2 = ['img', 'name', 'info', 'price', 'valute', 'type_food']

class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    info = State()
    price = State()
    valute = State()
    type_food = State()
    
class FSMadmin_replace(StatesGroup):
    replace_data = State()

#@dp.message_handler(commands=['admin_up'], is_chat_admin=True)
async def make_change_command(message: types.Message):
    global ID
    ID.append(message.from_user.id)
    await bot.send_message(message.from_user.id, 'Welcom admin!', reply_markup=admin_key.key_admin)
    await message.delete()
    await bot.send_message(message.from_user.id, 'Инструкция по использованию кнопок админа', reply_markup=InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton(text='Инструкция', callback_data='instruction')))

#@dp.callback_query_handler(Text(equals='instruction'))
async def admin_instruction(callback: types.CallbackQuery):    
    await callback.message.answer('КОМАНДЫ АДМИНА\n\n/Загрузить - команда для добавления товаров в меню. ВНИМАТЕЛЬНО ЧИТАЙТЕ СООБЩЕНИЯ БОТА ПРИ ВВОДЕ ДАННЫХ!!!\n\n/Изменить - команда для изменения отдельных характеристик товара. Всё что вам нужно, после ввода команды нажать на соответсвующие кнопки, под нужным товаром\n\n/Удалить - команда для удаления товаров в меню. Как и в команде "/Загрузить", всё что вам нужно, после ввода команды нажать на кнопку под нужным товаром')
    await callback.answer()


##########APEND##########

#@dp.message_handler(Text(equals='загрузить'), state=None) #commands=['Загрузить']
async def fs_admin(message : types.Message):
    if message.from_user.id in ID:
        await FSMadmin.photo.set()
        await message.reply('Загрузи фото')
        await message.answer('В случае отмены работы, отправьте сообщение "отмена"')

#@dp.message_handler(state="*", commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel(message : types.Message, state: FSMContext):
    if message.from_user.id in ID:
        stop_state = await state.get_state()
        if stop_state is None:
            return
        await state.finish()
        await message.reply('Всё в порядке/All right')

#@dp.message_handler(content_types=['photo'], state=FSMadmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply('Введите название')

#@dp.message_handler(state=FSMadmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            if len(message.text.encode('utf-8')) <= 64:
                data['name'] = message.text
            else:
                data['name'] = 'Не установлено'
                await message.reply('Вес названия превысил 64 байта, название не установлено')
        await FSMadmin.next()
        await message.reply('Расскажите подробнее о товаре')

#@dp.message_handler(state=FSMadmin.info)
async def load_info(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['info'] = message.text
        await FSMadmin.next()
        await message.reply('Введи цену (число без валюты)')

#@dp.message_handler(state=FSMadmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['price'] = await menu_price_piccer(message)
        await FSMadmin.next()
        await message.reply('Введите валюту')

#@dp.message_handler(state=FSMadmin.valute)
async def load_valute(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            data['valute'] = message.text
        await FSMadmin.next()    
        await message.reply('Введите тип товара:\n\n1)Пицца\n2)Закуска\n3)Напиток\nВВЕДИТЕ ЧИСЛО!')

#@dp.message_handler(state=FSMadmin.type_food)
async def load_type_food(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data:
            if message.text.isdigit() == True:
                data['type_food'] = message.text
            else:
                data['type_food'] = '1'
                await message.reply('Введён некорректный тип товара! Тип товара установлен по умолчанию: 1 - Пицца')
        await sqlite_data.sql_command(state)
        await state.finish()


##########REPLACE##########

#@dp.callback_query_handler(lambda y: y.data and y.data.startswith('replace '))   
async def replace_callback_run(callback: types.CallbackQuery, state: FSMContext):
    try:    
        await FSMadmin_replace.replace_data.set()
        async with state.proxy() as data_2:
            for ret_data in range(2):
                data_2[f'data_0_{ret_data}'] = callback.data.replace('replace ', '').split(' ')[ret_data]
        await callback.message.answer('Внесите изменения')
        await callback.answer()
    except Exception as e:
        print(f'\nException:\nID: {ID}\nreplace_callback_run: ', e, '\n')
        await callback.answer('Произошла ошибка, попробуйте заново', show_alert=True)

#@dp.message_handler(state=FSMadmin_replace.replace_data)
#@dp.message_handler(content_types=['photo'], state=FSMadmin_replace.replace_data)
async def replace_data(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        async with state.proxy() as data_2:
            if data_2['data_0_1'] == 'img':
                data_2_loc = message.photo[0].file_id
            elif data_2['data_0_1'] == 'price':
                data_2_loc = await menu_price_piccer(message)
            else:
                data_2_loc = message.text
            await sqlite_data.sql_replace_command([data_2['data_0_1'], 'number', data_2_loc, data_2['data_0_0']])
            await state.finish()
  
#@dp.message_handler(Text(equals='изменить')) #commands=['Изменить']
async def replace_items(message: types.Message):
    def list_keyboard(ret):
        return [InlineKeyboardButton(text=names[i], callback_data=f'replace {ret[0]} {names_2[i]}') for i in range(6)]
    if message.from_user.id in ID:
        read = await sqlite_data.sql_read()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[1], f'{ret[2]}\nОписание: {ret[3]}\nЦена: {ret[4]} {ret[5]}\nТип: {ret[-1]}')
            e = list_keyboard(ret)
            await bot.send_message(message.from_user.id, text='^^^Изменить^^^', reply_markup=InlineKeyboardMarkup(row_width=6).row(*e))


##########DELETE##########

#@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete '))
async def delete_callback_run(callback: types.CallbackQuery):
    await sqlite_data.sql_delete_command(callback.data.replace('delete ', ''))
    await callback.answer(text=f'{callback.data.replace("delete ", "")} was delete', show_alert=True)
    
#@dp.message_handler(Text(equals='удалить')) #commands=['Удалить']
async def delete_items(message: types.Message):
    if message.from_user.id in ID:
        read = await sqlite_data.sql_read()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[1], f'{ret[2]}\nОписание: {ret[3]}\nЦена: {ret[4]} {ret[5]}\nТип: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[2]}', callback_data=f'delete {ret[2]}')))



def check_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(make_change_command, commands=['admin_up'], is_chat_admin=True)
    dp.register_callback_query_handler(admin_instruction, Text(equals='instruction'))
    dp.register_message_handler(fs_admin, Text(equals='загрузить'), state=None)
    dp.register_message_handler(cancel, state="*", commands=['отмена', 'Отмена'])
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_info, state=FSMadmin.info)
    dp.register_message_handler(load_price, state=FSMadmin.price)
    dp.register_message_handler(load_type_food, state=FSMadmin.type_food)
    dp.register_message_handler(load_valute, state=FSMadmin.valute)
    dp.register_callback_query_handler(replace_callback_run, lambda y: y.data and y.data.startswith('replace '))
    dp.register_message_handler(replace_data, state=FSMadmin_replace.replace_data)
    dp.register_message_handler(replace_data, content_types=['photo'], state=FSMadmin_replace.replace_data)
    dp.register_message_handler(replace_items, Text(equals='изменить'))
    dp.register_callback_query_handler(delete_callback_run, lambda x: x.data and x.data.startswith('delete '))
    dp.register_message_handler(delete_items, Text(equals='удалить'))