# -*- coding:utf-8 -*-
import pygame
from pynput.keyboard import Key, Controller as keyboardController, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from time import sleep
import threading


"""
    Author: EK
    
    Version： 0.62
    Update: 增加在怪物区中心，自动原地转动角度寻怪并打怪内容 
    Date: 2019.11.18
    
    Version： 0.61
    Update: 合并挂机和打怪宏 
    Date: 2019.09.21
    
    
    is_run代表运行状态：
    run状态        按“鼠标中键”或“PageUP”进入run（开始运行）
    GJ和pause状态  按“F9”在GJ/pause两种状态之间切换（GJ代表挂机，pause代表暂停）
    stop状态       按“F11”进入stop（停止），经过EXIT_COUNT_DOWN秒后退出程序
"""


BEGIN_SOUND = r'begin_sound.mp3'
EXIT_SOUND = r'exit_sound.mp3'
EXIT_COUNT_DOWN = 3.5


# 播放开始音效
def play_sound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()


# 此action函数单独一个线程，根据不同的is_run状态，在这里状态执行对应动作
def action():
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
                    # keyboard.press('j')
                    # keyboard.release('j')
                    # sleep(0.6)
                    keyboard.press('i')
                    keyboard.release('i')
                    sleep(0.6)
                    # keyboard.press('c')
                    # keyboard.release('c')
                    # sleep(0.6)
        elif is_run == "stop":
            print("退出倒计时 %d 秒" % EXIT_COUNT_DOWN)
            sleep(EXIT_COUNT_DOWN)
            if is_run == "stop":
                return False
        elif is_run == "GJ":
            gj()
        sleep(0.8)


# 挂机方法
def gj():
    keyboard.press('w')
    keyboard.release('w')
    sleep(0.2)
    keyboard.press('a')
    keyboard.release('a')
    sleep(0.2)
    keyboard.press('s')
    keyboard.release('s')
    sleep(0.2)
    keyboard.press('d')
    keyboard.release('d')
    sleep(0.2)
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    sleep(0.2)
    with keyboard.pressed(Key.shift):
        keyboard.press('c')
        keyboard.release('c')
    sleep(1)


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
    # 按PageUP进入run，再按一次回到pause
    if key == Key.page_up:
        if is_run != "run":
            is_run = "run"
            play_sound(BEGIN_SOUND)
            print("开始")
        elif is_run == "run":
            is_run = "pause"
            play_sound(EXIT_SOUND)
            print("暂停")
    # 按F11退出，有
    elif key == Key.f11:
        is_run = "stop"
        play_sound(EXIT_SOUND)
    # 按F9进入GJ，再按一次回到pause
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
t3 = threading.Thread(target=action)
threads.append(t3)
# t3 = threading.Thread(target=buff)
# threads.append(t3)
# t4 = threading.Thread(target=buff_yizhi)
# threads.append(t4)
# print(threads)


if __name__ == '__main__':

    # 音乐播放方法初始化
    pygame.mixer.init()

    # 初始化is_run状态为 "pause" ，使运行程序后等待接收指令
    is_run = "pause"

    # 创建pynput.keyboard.Controller的实例（对象），才能调用方法
    keyboard = keyboardController()

    print("程序运行中，请输入命令（鼠标中键开始/暂停脚本，F11退出）：")
    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()
