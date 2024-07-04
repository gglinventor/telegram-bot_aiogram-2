from aiogram import types
from aiogram.utils import executor
from not_error import dp
from data_base import sqlite_data
#import sqlite3 as sql

async def on_startup(_):
    print('sucсessful start') 
    await sqlite_data.sql_start()
    await dp.bot.set_my_commands([types.BotCommand('start', 'Запуск бота'), types.BotCommand('menu', 'Вывод меню'), types.BotCommand('help', 'Помощь')]) #types.BotCommand('menu', 'Вывод меню')
    print('commands successful start')


from handlers import client, admin, other

client.check_handlers_client(dp)
admin.check_handlers_admin(dp)
other.check_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)