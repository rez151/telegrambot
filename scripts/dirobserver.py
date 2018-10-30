import csv
import glob
from time import sleep

# load sent pics from piclist.csv
from scripts.bilderbot import send_pictures

pic_list = []
with open("../piclist.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        pic_list.append(row[0])


# Python code t get difference of two lists
# Using set()
def diff(read_pics, saved_pics):
    return list(set(read_pics) - set(saved_pics))


def get_new_pics():
    pics = glob.glob("../bilder/*")

    new_pics = diff(pics, pic_list)
    print("new pics: " + str(new_pics))

    return new_pics


def add_to_list(new_pics):
    with open("../piclist.csv", "a") as f:
        writer = csv.writer(f)

        for pic in new_pics:
            writer.writerow([pic])
        pic_list.append(new_pics[0])


def send_new_pics(new_pics):
    print("sending new pics: " + str(new_pics))
    add_to_list(new_pics)


    '''
    HIER SENDE new_pics AN TELEGRAM GRUPPE ÜBER BOT
    '''
    send_pictures(new_pics)


def main():
    print(pic_list)

    while True:
        new_pics = get_new_pics()

        if len(new_pics) > 0:
            send_new_pics(new_pics)
        else:
            print("no new pics found")

        sleep(3)


if __name__ == "__main__":
    main()
