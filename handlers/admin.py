from aiogram import types
from misc import dp, bot
import sqlite3
from aiogram.dispatcher import FSMContext
from .sqlit import stata_user
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 941730379 #Бекир

ADMIN_ID =[ADMIN_ID_1,ADMIN_ID_2,ADMIN_ID_3]

class reg(StatesGroup):
    name = State()
    fname = State()

class reg0(StatesGroup):
    name0 = State()
    fname0 = State()

class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()
    step_q = State()
    step_regbutton = State()

@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_b = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
        bat_d = types.InlineKeyboardButton(text='База пользователей', callback_data='baza')
        markup.add(bat_a)
        markup.add(bat_b)
        markup.add(bat_d)
        await bot.send_message(message.chat.id,'Выбери что хочешь сделать:',reply_markup=markup)

@dp.callback_query_handler(text='baza')
async def baza1(call: types.callback_query):
    a = open('server.db','rb')
    await bot.send_document(chat_id=call.message.chat.id, document=a)

@dp.callback_query_handler(text='list_members')
async def admin_1(call: types.callback_query):
    status = stata_user()
    mes = await bot.send_message(call.message.chat.id, f'Всего пользователей: {status}')
    await asyncio.sleep(10)
    await bot.delete_message(message_id=mes.message_id,chat_id=call.message.chat.id)


########################  Рассылка  ################################

@dp.callback_query_handler(text='write_message')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                           reply_markup=murkap)
    await st_reg.step_q.set()


@dp.callback_query_handler(text='otemena',state='*')
async def otmena_12(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()



@dp.message_handler(state=st_reg.step_q,content_types=['text','photo','video','video_note']) # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    await st_reg.st_name.set()
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
    bat2 = types.InlineKeyboardButton(text='Добавить кнопки', callback_data='add_but')
    murkap.add(bat1)
    murkap.add(bat2)
    murkap.add(bat0)

    await message.copy_to(chat_id=message.chat.id)
    q = message
    await state.update_data(q=q)

    await bot.send_message(chat_id=message.chat.id,text='Пост сейчас выглядит так 👆',reply_markup=murkap)



# НАСТРОЙКА КНОПОК
@dp.callback_query_handler(text='add_but',state=st_reg.st_name) # Добавление кнопок
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id,text='Отправляй мне кнопки по принципу Controller Bot\n\n'
                                                     'Пока можно добавить только одну кнопку')
    await st_reg.step_regbutton.set()


@dp.message_handler(state=st_reg.step_regbutton,content_types=['text']) # Текст кнопок в неформате
async def redarkt_button(message: types.Message, state: FSMContext):
    arr2 = message.text.split('-')

    k = -1  # Убираем пробелы из кнопок
    for i in arr2:
        k+=1
        if i[0] == ' ':
            if i[-1] == ' ':
                arr2[k] = (i[1:-1])
            else:
                arr2[k] = (i[1:])

        else:
            if i[-1] == ' ':

                arr2[0] = (i[:-1])
            else:
                pass

    # arr2 - Массив с данными


    try:
        murkap = types.InlineKeyboardMarkup() #Клавиатура с кнопками
        bat = types.InlineKeyboardButton(text= arr2[0], url=arr2[1])
        murkap.add(bat)

        data = await state.get_data()
        mess = data['q']  # ID сообщения для рассылки

        await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,message_id=mess.message_id,reply_markup=murkap)

        await state.update_data(text_but =arr2[0]) # Обновление Сета
        await state.update_data(url_but=arr2[1])  # Обновление Сета

        murkap2 = types.InlineKeyboardMarkup() # Клавиатура - меню
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
        murkap2.add(bat1)
        murkap2.add(bat0)

        await bot.send_message(chat_id=message.chat.id,text='Теперь твой пост выглядит так☝',reply_markup=murkap2)


    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()


# КОНЕЦ НАСТРОЙКИ КНОПОК


@dp.callback_query_handler(text='send_ras',state="*") # Рассылка
async def fname_step(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

    data = await state.get_data()
    mess = data['q'] # Сообщения для рассылки

    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками

    try: #Пытаемся добавить кнопки. Если их нету оставляем клаву пустой
        text_but = data['text_but']
        url_but = data['url_but']
        bat = types.InlineKeyboardButton(text=text_but, url=url_but)
        murkap.add(bat)
    except: pass


    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time").fetchall()
    bad = 0
    good = 0
    await bot.send_message(call.message.chat.id, f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        await asyncio.sleep(1)
        try:
            await mess.copy_to(i[0],reply_markup=murkap)
            good += 1
        except:
            bad += 1

    await bot.send_message(
        call.message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )
#########################################################