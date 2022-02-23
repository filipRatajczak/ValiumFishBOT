import logging
import threading
import time
from random import random, randint

import win32con
import win32gui

from AI.DigitRecognizer import create_nparray_from_picture, predict_single_input, create_cnn_model
from ClientCrawler import ReadProcessMemory
from FishingLogic.Key import PressKey, ReleaseKey
from Screenshots import Screenshoter, ImageCroper

global IS_FLAG_STACK
global IS_FLAG_IDLE


def use_worm():
    key = randint(59, 62)
    PressKey(key)
    time.sleep(random() / 2)
    ReleaseKey(key)


def use_fishing_rod():
    PressKey(0x39)
    time.sleep(random() / 2)
    ReleaseKey(0x39)


def press_space():
    PressKey(0x39)
    time.sleep(random() / 5)
    ReleaseKey(0x39)


def press_space_x_times(x):
    for i in range(x):
        time.sleep(random() / 10)
        press_space()


def initial_fishing():
    use_worm()
    time.sleep(random() / 2)
    use_fishing_rod()


def get_windows_placement(window_id):
    return win32gui.GetWindowPlacement(window_id)[1]


def set_active_window(hwnd):
    if get_windows_placement(hwnd) == 2:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    else:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetActiveWindow(hwnd)


def go_fishing(handle):
    logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info(f'VALIUM FISH-BOT STARTED')
    model = create_cnn_model()
    hwnd = win32gui.FindWindow(None, "Valium.pl")
    set_active_window(hwnd)
    initial_fishing()

    while True:
        isFish = ReadProcessMemory.get_fishing_flag(handle)
        time.sleep(random())
        if isFish == 1:
            logging.info(f'FLAG IS SET TO 1')
            fishing_content(hwnd, model)


def check_on_flag_stacked(handle):
    while True:
        isFish = ReadProcessMemory.get_fishing_flag(handle)
        if isFish == 1:
            time.sleep(random())
            start_time = time.time()
            while isFish == 1:
                isFish = ReadProcessMemory.get_fishing_flag(handle)
                time.sleep(random())
                stop_time = time.time()
                if int(stop_time - start_time) > 60:
                    logging.warning(
                        f'SEEMS FISH-BOT GOT STACKED WHEN FLAG = {isFish} FOR {(stop_time - start_time)} SECONDS, TRYING TO REPAIR IT...')
                    initial_fishing()
                    time.sleep(60 + random())
                    break


def check_off_flag_stacked(handle):
    while True:
        isFish = ReadProcessMemory.get_fishing_flag(handle)
        if isFish == 253:
            time.sleep(random())
            start_time = time.time()
            while isFish == 253:
                isFish = ReadProcessMemory.get_fishing_flag(handle)
                time.sleep(random())
                stop_time = time.time()
                if int(stop_time - start_time) > 60:
                    logging.warning(
                        f'SEEMS FISH-BOT GOT STACKED WHEN FLAG = {isFish} FOR {(stop_time - start_time)} SECONDS, TRYING TO REPAIR IT...')
                    initial_fishing()
                    time.sleep(60 + random())
                    break


def fishing_content(hwnd, model):
    take_screenshot_and_crop(hwnd)
    num_of_spaces_to_click = get_number_from_model(model)
    set_active_window(hwnd)
    press_space_x_times(num_of_spaces_to_click)
    time.sleep(8 + random())
    use_worm()
    use_fishing_rod()


def get_number_from_model(model):
    data = create_nparray_from_picture(
        "C:\\Users\\Filip\\PycharmProjects\\ValiumFishbot\\FishingLogic\\$screenshot.bmp")
    num_of_spaces_to_click = predict_single_input(data, model)
    logging.info(f'I PREDICTED: {num_of_spaces_to_click}')
    return num_of_spaces_to_click


def take_screenshot_and_crop(hwnd):
    file_name = 'screenshot'
    Screenshoter.create_background_screenshot(hwnd, 680, 510, file_name)
    ImageCroper.crop_image(file_name)


if __name__ == '__main__':
    handle = ReadProcessMemory.get_valium_process_object_details()

    stacked = threading.Thread(target=check_on_flag_stacked, args=(handle,))
    idle = threading.Thread(target=check_off_flag_stacked, args=(handle,))
    bot = threading.Thread(target=go_fishing, args=(handle,))
    bot.start()
    time.sleep(180)
    stacked.start()
    idle.start()
