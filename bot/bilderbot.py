import csv
import datetime
import logging

import requests
from telegram import Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

from observer.dirobserver import start_observer

token = "650563487:AAGb6cR_hieWNFcOfbyN_1oUkvs5t4lCi40"
chat_id = 755671327

updater = Updater(token=token)
job_queue = updater.job_queue
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def add_to_subscribers(chat_id):
    with open("../subscriber.csv", newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) > 0:
                if int(row[0]) == int(chat_id):
                    print("chat_id " + row[0] + " already subscribed")
                    return

    with open("../subscriber.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([str(chat_id)])
        print("subscriber added with chat_id: " + str(chat_id))


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Willkommen auf der Hochzeit des Jahres! Ich versorge euch mit den schönsten Bildern. Viel Spaß!!")

    bot.send_message(chat_id=update.message.chat_id,
                     text="Möchtest du alle Bilder herunterladen die bis jetzt gemacht wurden? Schreibe mir dazu /bilder")

    bot.send_message(chat_id=update.message.chat_id,
                     text="Falls du Bilder mit allen Gästen teilen möchtest, schicke sie mir einfach.")

    add_to_subscribers(update.message.chat_id)


def get_pics_until(current_time):
    missed_pics = []

    with open('../piclist.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] < str(current_time):
                missed_pics.append(row[0])

    return missed_pics


def send_previous(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Ich schicke dir jetzt alle Bilder die du verpasst hast.")

    current_time = datetime.datetime.now()

    missed_pics = get_pics_until(current_time)

    # send pics
    url = "https://api.telegram.org/bot" + token + "/sendPhoto"
    data = {'chat_id': update.message.chat_id}

    for pic in missed_pics:
        files = {'photo': open(pic, 'rb')}
        r = requests.post(url, files=files, data=data)
        print(r.status_code, r.reason, r.content)

    bot.send_message(chat_id=update.message.chat_id,
                     text="Du bist nun auf dem aktuellen Stand.")


def forward_photo(bot, update):
    print(bot)
    print(update)
    photo_id = update.message.photo[3].file_id

    with open("../subscriber.csv", newline='') as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) > 0:
                if not int(row[0]) == update.message.chat_id:
                    current_chat_id = int(row[0])
                    bot.send_photo(chat_id=current_chat_id, photo=photo_id,
                                   caption="von " + update.message.from_user.first_name)


def echo(bot, update):
    bot.send_message(chat_id=chat_id,
                     text="deine chat_id ist: " + chat_id)


start_handler = CommandHandler('start', start)
echo_handler = CommandHandler('echo', echo)
send_previous_handler = CommandHandler('bilder', send_previous)
forward_handler = MessageHandler(Filters.photo, forward_photo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(send_previous_handler)
dispatcher.add_handler(forward_handler)

updater.start_polling()
start_observer()
