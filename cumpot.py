import telebot
from pornhub_api import PornhubApi
import random
from telebot import types
bot = telebot.TeleBot('1360141455:AAEz5hbGuCg4Mv5Aqa4bHRT1kcvQOVHIRSI')
api = PornhubApi()

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        markup = types.ReplyKeyboardMarkup()
        markup.row('компот', 'рандом')
        bot.send_message(message.from_user.id, "Привет, я бот компот!")
        bot.send_message(message.from_user.id, "Воспользуйся кнопками ниже, чтобы найти лучшие видео в интернете 😏", reply_markup=markup)
    elif message.text == "компот":
        bot.send_message(message.from_user.id, "Напиши категорию")
        bot.register_next_step_handler(message, get_tag_messages)
    elif message.text == "рандом":
        count = 0
        tags = random.sample(api.video.tags("f").tags, 5)
        category = random.choice(api.video.categories().categories)
        result = api.search.search(ordering="mostviewed", tags=tags, category=category)

        for vid in result.videos:
            if count == 1:
                break
            bot.send_message(message.from_user.id, vid.url)
            count += 1
    elif message.text == "илья":
        bot.send_message(message.from_user.id, "камень🗿")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'more':
        bot.send_message(call.message.chat.id, "Напиши категорию")
        bot.register_next_step_handler(call.message, get_tag_messages)

def get_tag_messages(message):
    count = 0
    data = api.search.search(
        ordering="mostviewed",
        period="weekly",
        tags=[message.text],
    )
    for i in range(2):
        vid = random.choice(data.videos)
        bot.send_message(message.from_user.id, vid.url)
    #Добавление кнопки "ещё"
    markup = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='Ещё', callback_data='more')
    markup.add(btn_my_site)

    vid = random.choice(data.videos)
    bot.send_message(message.from_user.id, vid.url, reply_markup = markup)

bot.polling(none_stop=True, interval=0)
