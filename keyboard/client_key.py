from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

but_1 = KeyboardButton('частые вопросы')
but_2 = KeyboardButton('тех поддержка')
but_3 = KeyboardButton('меню')
but_4 = KeyboardButton('отзывы')
but_5 = KeyboardButton('Поделиться номером', request_contact=True)
but_6 = KeyboardButton('Отправить местоположение', request_location=True)


key_client = ReplyKeyboardMarkup(resize_keyboard=True)

key_client.row(but_1, but_2).row(but_3, but_4).row(but_5, but_6)