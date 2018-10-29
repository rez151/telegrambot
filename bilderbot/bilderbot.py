import glob
from time import sleep

pic_list = []


# Python code t get difference of two lists
# Using set()
def diff(read_pics, saved_pics):
    return list(set(read_pics) - set(saved_pics))


def get_new_pics():
    print("get pics")
    pics = glob.glob("../bilder/*")

    new_pics = diff(pics, pic_list)

    print("new pics: " + str(new_pics))

    return new_pics


def add_to_list(new_pics):
    with open("../piclist.txt") as f:
        for pic in new_pics:
            f.write(str(pic))


def send_new_pics(new_pics):
    print("sending new pics: " + str(new_pics))
    add_to_list(new_pics)


def main():
    with open("../piclist.txt") as f:
        pic_list = f.readlines()

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
