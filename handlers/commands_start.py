from aiogram import types
from misc import dp,bot
import sqlite3
from .sqlit import reg_user
from aiogram.dispatcher import FSMContext
from .sqlit import stata_user
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

photo_start = 'AgACAgIAAxkBAAMCYQQ9IRTpUmX8H-NLoskP5QcB5TIAAle0MRsg6yBImTANjDylYWEBAAMCAAN5AAMgBA'# Нажал старт


class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message,state: FSMContext):
    reg_user(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    bat1 = types.InlineKeyboardButton(text='🚀Стартовать🚀', callback_data='start_go')
    markup.add(bat1)

    await bot.send_photo(message.chat.id,photo=photo_start,caption = """<b>Воооу привет!👋👋👋</b>

Это бот для подготовки к запуску спринта 🚀

Тебе будет отправлено 3️⃣ обучающих видео после каждого из них необходимо выполнить задание и отправить его в бота. 

<i>После успешного прохождения бота ты будешь зачислен в чат, где начнешь работать с Тик Током🔥🔥🔥</i>""",reply_markup=markup,parse_mode='html')
