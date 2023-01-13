import telebot
from telebot import types
API_TOKEN = '5800681265:AAHeJ-aPEZP_yeTnLv_nXyAjT6ghYTgnylM'
bot = telebot.TeleBot(API_TOKEN)
name = ''
surname = ''
city = ''

"""
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем могу помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
"""


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Какая твоя фамилия?")
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_moscow = types.InlineKeyboardButton(text='Москва', callback_data='Moscow')
    keyboard.add(key_moscow)
    key_spb = types.InlineKeyboardButton(text='Санкт-Петербург', callback_data='SPB')
    keyboard.add(key_spb)
    key_other = types.InlineKeyboardButton(text='Другое', callback_data='other')
    keyboard.add(key_other)
    bot.send_message(message.from_user.id, text='Выбери город', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global city
    if call.data == 'other':
        bot.send_message(call.message.chat.id, 'Извини, мы не работаем в других городах.')
    else:
        if call.data == 'Moscow':
            city = 'Москва'
        if call.data == 'SPB':
            city = 'Санкт-Петербург'
        info = '\nИмя:' + str(name) + '\nФамилия:' + str(surname) + '\nГород:' + str(city)
        bot.send_message(call.message.chat.id, info)
        reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        reply_keyboard.add(btn1, btn2)
        bot.send_message(call.from_user.id, text='Все верно?', reply_markup=reply_keyboard)

@bot.message_handler(content_types=['text'])
def callback2(message):
    if message.text == 'Да':
        bot.send_message(message.from_user.id, text='Хорошо')
    else:
        bot.send_message(message.from_user.id, text='Плохо')
"""
@bot.message_handler()
def check(message):
    reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    reply_keyboard.add(btn1, btn2)
    bot.send_message(message.from_user.id, text='Все верно?', reply_markup=reply_keyboard)
    if message.text == 'Да':
        bot.send_message(message.from_user.id, text='Хорошо')
    else:
        bot.send_message(message.from_user.id, text='Плохо')
"""

bot.polling(none_stop=True, interval=0)
