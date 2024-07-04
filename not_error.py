from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

storage=MemoryStorage()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)