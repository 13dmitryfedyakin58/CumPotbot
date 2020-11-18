import telebot
from pornhub_api import PornhubApi
import random
from telebot import types
bot = telebot.TeleBot('1360141455:AAEz5hbGuCg4Mv5Aqa4bHRT1kcvQOVHIRSI');
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши компот")
    elif message.text == "компот":
        bot.send_message(message.from_user.id, "Напиши категорию")
        bot.register_next_step_handler(message, get_tag_messages)
    elif message.text == "рандом":
        api = PornhubApi()
        count = 0
        tags = random.sample(api.video.tags("f").tags, 5)
        category = random.choice(api.video.categories().categories)
        result = api.search.search(ordering="mostviewed", tags=tags, category=category)

        for vid in result.videos:
            if count == 1:
                break
            bot.send_message(message.from_user.id, vid.url)
            count += 1
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

def get_tag_messages(message):
    count = 0
    api = PornhubApi()
    data = api.search.search(
        ordering="mostviewed",
        period="weekly",
        tags=[message.text],
    )
    for vid in data.videos:
        if count == 3:
            break
        bot.send_message(message.from_user.id, vid.url)
        count += 1
bot.polling(none_stop=True, interval=0)
