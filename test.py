from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import time
import keyboard

def on_exit(icon, item):
    icon.stop()
    exit()

def on_alt_k(event):
    if event.event_type == keyboard.KEY_DOWN and event.name == 'alt' and 'k' in keyboard._pressed_events:
        print("Alt + K 눌림")

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

    # 백그라운드 작업을 위한 스레드 생성
    background_thread = threading.Thread(target=background_task)

    # 백그라운드 스레드를 데몬 스레드로 설정 (메인 스레드 종료시 함께 종료)
    background_thread.daemon = True

    # 백그라운드 스레드 시작
    background_thread.start()

    # Alt + K 단축키를 감지하는 훅 설정
    keyboard.hook(on_alt_k)

    # 아이콘을 태스크 바에 표시
    icon.run()

if __name__ == "__main__":
    main()
