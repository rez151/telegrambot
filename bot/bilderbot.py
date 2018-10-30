import logging

from telegram.ext import Updater, CommandHandler

from observer.dirobserver import start_observer

token = "650563487:AAGb6cR_hieWNFcOfbyN_1oUkvs5t4lCi40"
chat_id = 755671327

updater = Updater(token=token)
job_queue = updater.job_queue
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Willkommen auf der Hochzeit des Jahres! Ich versorge euch mit den schönsten Bildern. Viel Spaß!!")
    print(update.message.chat_id)


def echo(bot, update):
    bot.send_message(chat_id=chat_id,
                     text="id passt")


start_handler = CommandHandler('start', start)
echo_handler = CommandHandler('echo', echo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling()
start_observer()
