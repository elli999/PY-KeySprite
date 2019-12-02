# -*- coding:utf-8 -*-
import pygame
from pynput.keyboard import Key, Controller as keyboardController, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from time import sleep
import threading


"""
    Author: EK
    Update: 合并挂机和打怪宏 
    Date: 2019.09.21
    
    is_run代表运行状态，pause代表暂停，run代表运行，GJ代表挂机，stop代表结束程序
"""


BEGIN_SOUND = r'begin_sound.mp3'
EXIT_SOUND = r'exit_sound.mp3'
EXIT_COUNT_DOWN = 3.5


def play_sound(sound):
    # 播放开始音效
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()


def key_pressing():
    # 按键脚本实质内容， is_run == "pause" 时无动作（暂停等待）
    print("开始脚本！")
    # global is_run
    while True:
        if is_run == "run":
            # for i in range(0, 60):
            # with keyController.pressed(Key.shift):
            #     keyController.press('n')
            #     keyController.release('n')
            while True:
                if is_run == "pause":
                    break
                elif is_run == "stop":
                    print("退出倒计时 %d 秒" % EXIT_COUNT_DOWN)
                    sleep(EXIT_COUNT_DOWN)
                    if is_run == "stop":
                        return False
                elif is_run == "GJ":
                    gj()
                elif is_run == "run":
                    keyController.press('j')
                    keyController.release('j')
                    sleep(0.6)
                    keyController.press('i')
                    keyController.release('i')
                    sleep(0.6)
                    keyController.press('c')
                    keyController.release('c')
                    sleep(0.6)
        elif is_run == "stop":
            print("退出倒计时 %d 秒" % EXIT_COUNT_DOWN)
            sleep(EXIT_COUNT_DOWN)
            if is_run == "stop":
                return False
        elif is_run == "GJ":
            gj()
        sleep(0.8)


def gj():
    keyController.press(Key.space)
    keyController.release(Key.space)
    sleep(1.5)
    keyController.press('d')
    sleep(0.8)
    keyController.release('d')
    sleep(0.8)
    keyController.press('a')
    sleep(0.8)
    keyController.release('a')
    sleep(0.4)


def on_click(x, y, button, pressed):
    print("{0} {1}.".format(button.name, pressed))
    global is_run
    if button.name == "middle" and pressed is True:
        if is_run != "run":
            is_run = "run"
            play_sound(BEGIN_SOUND)
            print("开始")
        elif is_run == "run":
            is_run = "pause"
            play_sound(EXIT_SOUND)
            print("暂停")


# def on_scroll(x, y, dx, dy):
#     print(x, y, dx, dy)
#     global is_run
#     # dy 代表滚轮的y轴方向。当dy == 1时，滚轮向上滚动一次，dy == -1时，滚轮向下滚动一次。
#     if dy == -1:
#         is_run = 0
#         play_sound(EXIT_SOUND)
#         print("暂停")


def on_release(key):
    print("按键 %s " % key)
    global is_run
    if key == Key.page_up:
        if is_run != "run":
            is_run = "run"
            play_sound(BEGIN_SOUND)
            print("开始")
        elif is_run == "run":
            is_run = "pause"
            play_sound(EXIT_SOUND)
            print("暂停")
    elif key == Key.f11:
        is_run = "stop"
        play_sound(EXIT_SOUND)
    elif key == Key.f9:
        if is_run != "GJ":
            is_run = "GJ"
            play_sound(EXIT_SOUND)
        elif is_run == "GJ":
            is_run = "pause"
            play_sound(EXIT_SOUND)


def mouse_listen():
    with MouseListener(on_click=on_click) as listener:
        listener.join()


def keyboard_listen():
    with KeyboardListener(on_release=on_release) as listener:
        listener.join()


# def buff():
#     while is_run == 1:
#         sleep(BUFF_INTERVAL)
#         keyController.press('[')
#         keyController.release('[')
#         sleep(1.1)
#         keyController.press(']')
#         keyController.release(']')
#         sleep(1.1)


# def buff_yizhi():
#     while is_run == 1:
#         sleep(YIZHI_INTERVAL)
#         keyController.press('\\')
#         keyController.release('\\')


threads = []
t1 = threading.Thread(target=mouse_listen)
threads.append(t1)
t2 = threading.Thread(target=keyboard_listen)
threads.append(t2)
t3 = threading.Thread(target=key_pressing)
threads.append(t3)
# t3 = threading.Thread(target=buff)
# threads.append(t3)
# t4 = threading.Thread(target=buff_yizhi)
# threads.append(t4)
# print(threads)


if __name__ == '__main__':
    pygame.mixer.init()
    keyController = keyboardController()
    is_run = "pause"
    print("程序运行中，请输入命令（鼠标中键开始/暂停脚本，F11退出）：")
    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()
