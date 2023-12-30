from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import time
import keyboard

def on_exit(icon, item):
    icon.stop()
    exit()

def on_ctrl_k(event):
    if keyboard.read_key() == "p":
        print("You pressed p")

def background_task():
    while True:
        # 주기적으로 수행할 작업을 여기에 추가
        print("백그라운드 작업 수행 중...")
        time.sleep(5)  # 5초 대기

def create_icon():
    image = Image.open("R.png")
    menu = (Menu(MenuItem('Exit', on_exit),))

    icon = Icon("name", image, menu=menu)
    return icon

def main():
    icon = create_icon()
    icon.run()
    while True:
        if keyboard.read_key() == "p":
            print("You pressed p")

if __name__ == "__main__":
    main()
