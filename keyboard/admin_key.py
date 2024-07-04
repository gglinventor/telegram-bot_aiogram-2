from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

but_load = KeyboardButton('загрузить')
but_replace = KeyboardButton('изменить')
but_delete = KeyboardButton('удалить')

key_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(but_load, but_replace, but_delete)