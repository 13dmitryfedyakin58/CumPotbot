import telebot
from pornhub_api import PornhubApi

bot = telebot.TeleBot('1360141455:AAEz5hbGuCg4Mv5Aqa4bHRT1kcvQOVHIRSI');
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, я готов скинуть тебе CUMпот!")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text == "компот":
        #bot.send_message(message.from_user.id, "Напиши категорию")
        tag = get_text_messages("Напиши категорию")
        print(tag)
        count = 0
        api = PornhubApi()
        data = api.search.search(
            ordering="mostviewed",
            period="weekly",
            tags=[tag],
        )
        for vid in data.videos:
            if count == 3:
                break
            bot.send_message(message.from_user.id, vid.url)
            count += 1

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling(none_stop=True, interval=0)