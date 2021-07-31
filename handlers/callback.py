from aiogram import types
from misc import dp, bot
import sqlite3
from aiogram.dispatcher import FSMContext
from .sqlit import update_user
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

time_1 = 180 # ЗАдержка 180 cекунд
time_2 = 480 # ЗАдержка 480 cекунд
time_3 = 480 # ЗАдержка 480 cекунд

text_fast = """<b>Не хитри!</b>
Сначала посмотри видео, выполни домашку и скинь скрин!"""


video_note1 = 'DQACAgIAAxkBAAMDYQQ9n5qor9TJKiyfUBHA70WMmDIAAvkNAALvWSFIY2wVXyLDSPUgBA'

video1 = "BAACAgIAAxkBAAMJYQQ-_zPI5mnlo0iFdIpjyzNrwlAAAhMQAAKNDiBIxVtzGig65EUgBA"
video2 = 'BAACAgIAAxkBAAMcYQRCBZomh9vUryXpW99om8OGUHwAAh4QAAKNDiBI1nTqdiygXeYgBA'
video3 = "BAACAgIAAxkBAAMpYQRFE1S4rsnCSfaM526z18nmT60AAikQAAKNDiBIRLKD5QMgLCUgBA"

photo1 = "AgACAgIAAxkBAAMqYQRHimHnK4ecSV0oIJaLUFcFXFwAAui1MRuNDiBIIvJ83Oub5EoBAAMCAANzAAMgBA" # Конечное фото
class regs(StatesGroup):
    names = State()
    fnames = State()
    url_step = State()
    get_kod = State()

@dp.callback_query_handler(text='start_go')
async def start_go1(call: types.callback_query,state: FSMContext):
    await regs.names.set()
    await bot.send_video_note(chat_id=call.message.chat.id,video_note=video_note1)
    await bot.send_video(chat_id=call.message.chat.id,video=video1,caption="""Можешь посмотреть это видео в <a href="https://youtu.be/pmeY8ByIEPg">YouTube</a> <i>👈нажимать сюда</i> 

Сервис который использовался в видео https://www.freepik.com/

<u>Задание:</u> <b>Создать и оформить телеграм канал.</b>

<i>После того как выполнишь данное задание сделай скриншот канала и <b>отправь</b> его прямо <b>в бота!</b></i>

<pre>Служба поддержки</pre> <b><u>@JaysonAdmin</u>"</b>""",parse_mode='html')
    await state.update_data(p1 = '0')
    await asyncio.sleep(time_1)
    await state.update_data(p1= '1')




@dp.message_handler(state=regs.names, content_types=['photo','document'])
async def domashka_1(message: types.Message, state: FSMContext):
    p = (await state.get_data())['p1']
    if p == '0':
        await bot.send_message(message.chat.id,text=text_fast,parse_mode='html')
    else:
        await regs.fnames.set()
        await bot.send_video(chat_id=message.chat.id, video=video2,caption="""Можешь посмотреть это видео в <a href="https://youtu.be/NHUPaFJ9SmA">YouTube</a> <i>👈нажимать сюда</i>
    
<i>Сервисы которые использовались в видео:</i>
⚙️Controller Bot - https://t.me/ControllerBot
⚙️Сайт с фильмами - https://videocdn.tv/
⚙️Аналитика Телеметр - https://t.me/telemetrmebot
    
    
<u>Задание:</u> <b>Заполнить контентом (фильмами) свой телеграм канал и подать запрос на подключение аналитики Telemetr.</b>
    
<i>После того как выполнишь данное задание сделай скриншот канала и <b>отправь</b> его прямо <b>в бота!</b></i>
    
<pre>Служба поддержки</pre> <b><u>@JaysonAdmin</u>"</b>""",parse_mode='html')

        await state.update_data(p2='0')
        await asyncio.sleep(time_2)
        await state.update_data(p2='1')


@dp.message_handler(state=regs.fnames, content_types=['photo','document'])
async def domashka_2(message: types.Message, state: FSMContext):
    p = (await state.get_data())['p2']
    if p == '0':
        await bot.send_message(message.chat.id,text=text_fast,parse_mode='html')

    else:
        await regs.get_kod.set()
        await bot.send_video(chat_id=message.chat.id, video=video3, caption="""Можешь посмотреть это видео в <a href="https://youtu.be/4xaEvuU97J4">YouTube</a> <i>👈нажимать сюда</i>

<i>Сервис который использовался в видео:</i>
📲Сайт для скачивания видео - https://ru.savefrom.net/


<u>Задание:</u> <b>Посмотреть видео и нарезать 1 трейлер.</b>

<i>После того как выполнишь данное задание сделай скриншот из галереи с нарезками и <b>отправь</b> его прямо <b>в бота!</b></i>

<pre>Служба поддержки</pre> <b><u>@JaysonAdmin</u>"</b>""", parse_mode='html')
        await state.update_data(p3='0')
        await asyncio.sleep(time_3)
        await state.update_data(p3='1')

@dp.message_handler(state=regs.get_kod, content_types=['photo','document'])
async def domashka_3(message: types.Message, state: FSMContext):
    p = (await state.get_data())['p3']
    if p == '0':
        await bot.send_message(message.chat.id,text=text_fast,parse_mode='html')

    else:
        await state.finish()
        await bot.send_photo(chat_id=message.chat.id, photo=photo1, caption="""<b>Для завершения предварительного обучения необходимо создать "прокладку"</b> <pre>(специализированный канал с ботом)</pre>
    
Для создания "прокладки" <b>напиши</b> @JaysonAdmin кодовое слово <pre>СПРИНТ</pre> и <b>отправь ссылку</b> на свой канал с фильмами.""", parse_mode='html')