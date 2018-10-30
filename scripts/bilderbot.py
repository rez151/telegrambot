import logging

import requests
from telegram import update
from telegram.ext import Updater, CommandHandler

updater = Updater(token='650563487:AAGb6cR_hieWNFcOfbyN_1oUkvs5t4lCi40')
job_queue = updater.job_queue
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Willkommen auf der Hochzeit des Jahres! Ich versorge euch mit den schönsten Bildern. Viel Spaß!!")
    print(update.message.chat_id)


def echo(bot, update):
    bot.send_message(chat_id=755671327,
                     text="id passt")


start_handler = CommandHandler('start', start)
echo_handler = CommandHandler('echo', echo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)


def send_pictures(pics):
    token = '650563487:AAGb6cR_hieWNFcOfbyN_1oUkvs5t4lCi40'

    # filename = '/home/resi/PycharmProjects/telegrambot/zwischenspeicher/ibg.jpg'

    url = "https://api.telegram.org/bot" + token + "/sendPhoto"
    data = {'chat_id': "755671327"}

    for pic in pics:
        files = {'photo': open(pic, 'rb')}
        r = requests.post(url, files=files, data=data)
        print(r.status_code, r.reason, r.content)


updater.start_polling()
