import logging
import time
from random import random

import win32gui

from AI.DigitRecognizer import create_cnn_model, get_number_from_model
from Client.Clicker import press_random_f1_to_f4, press_space, press_space_x_times
from Client.MemoryReader import get_fishing_flag
from Screen.Screenshoter import take_screenshot_and_crop, set_focus_on_window

SPACE = 0x39
F1 = 0x3B
F4 = 0X3E
CONST_TIME_TO_RETRIEVE_FISH = 8
MINUTE_IN_SECONDS = 60
DEFAULT_SCREENSHOT_NAME = 'screenshot'
DEFAULT_SCREENSHOT_NAME_WITH_EXTENSION = 'screenshot.bmp'


def initial_fishing():
    press_random_f1_to_f4()
    time.sleep(random() / 2)
    press_space()


def fishing(handle, flag_value):
    logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info(f'VALIUM FISH-BOT STARTED')
    model = create_cnn_model()
    hwnd = win32gui.FindWindow(None, "Valium.pl")
    initial_fishing()

    counter = 0

    while True:
        isFish = get_fishing_flag(handle)
        time.sleep(random())
        if isFish == flag_value:
            logging.info(f'FLAG IS SET TO {flag_value}')
            fishing_content(hwnd, model)
            counter = counter + 1


def fishing_content(hwnd, model):
    take_screenshot_and_crop(hwnd, DEFAULT_SCREENSHOT_NAME)
    predicted_number = get_number_from_model(DEFAULT_SCREENSHOT_NAME_WITH_EXTENSION, model)
    set_focus_on_window(hwnd)
    press_space_x_times(predicted_number)
    time.sleep(CONST_TIME_TO_RETRIEVE_FISH + random())
    press_random_f1_to_f4()
    press_space()


def check_flag_stacked(handle, flag_value):
    hwnd = win32gui.FindWindow(None, "Valium.pl")

    while True:
        isFish = get_fishing_flag(handle)
        if isFish == flag_value:
            time.sleep(random())
            start_time = time.time()
            check_idle(flag_value, handle, isFish, start_time, hwnd)


def check_idle(flag_value, handle, isFish, start_time, hwnd):
    while isFish == flag_value:
        isFish = get_fishing_flag(handle)
        time.sleep(random())
        stop_time = time.time()
        if stop_time - start_time > MINUTE_IN_SECONDS:
            logging.warning(
                f'SEEMS FISH-BOT GOT STACKED WHEN FLAG = {isFish} FOR {(stop_time - start_time)} SECONDS, TRYING TO REPAIR IT...')
            set_focus_on_window(hwnd)
            initial_fishing()
            time.sleep(MINUTE_IN_SECONDS + random())


def collecting_screenshots(handle, flag_value):
    hwnd = win32gui.FindWindow(None, "Valium.pl")
    counter = 0
    while True:
        isFish = get_fishing_flag(handle)
        if isFish == flag_value:
            take_screenshot_and_crop(hwnd, f'{DEFAULT_SCREENSHOT_NAME}{counter}')
            counter = counter + 1
        time.sleep(CONST_TIME_TO_RETRIEVE_FISH + random())
