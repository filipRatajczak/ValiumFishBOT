import logging
import time
from random import random

import win32gui

from AI.DigitRecognizer import create_cnn_model, get_number_from_model, create_nparray_from_picture
from Client.Clicker import random_f1_to_f4, press_space, press_space_x_times
from Client.MemoryReader import get_fishing_flag
from Screen.Screenshoter import take_screenshot_and_crop

SPACE = 0x39
F1 = 0x3B
F4 = 0X3E
CONST_TIME_TO_RETRIEVE_FISH = 8
MINUTE_IN_SECONDS = 60


def initial_fishing():
    random_f1_to_f4()
    time.sleep(random() / 2)
    press_space()


def go_fishing(handle):
    logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info(f'VALIUM FISH-BOT STARTED')
    model = create_cnn_model()
    hwnd = win32gui.FindWindow(None, "Valium.pl")
    initial_fishing()

    while True:
        isFish = get_fishing_flag(handle)
        time.sleep(random())
        if isFish == 1:
            logging.info(f'FLAG IS SET TO 1')
            fishing_content(hwnd, model)


def check_flag_stacked(handle, flag_value):
    while True:
        isFish = get_fishing_flag(handle)
        if isFish == flag_value:
            time.sleep(random())
            start_time = time.time()
            check_idle(flag_value, handle, isFish, start_time)


def check_idle(flag_value, handle, isFish, start_time):
    while isFish == flag_value:
        isFish = get_fishing_flag(handle)
        time.sleep(random())
        stop_time = time.time()
        if stop_time - start_time > MINUTE_IN_SECONDS:
            logging.warning(
                f'SEEMS FISH-BOT GOT STACKED WHEN FLAG = {isFish} FOR {(stop_time - start_time)} SECONDS, TRYING TO REPAIR IT...')
            initial_fishing()
            time.sleep(MINUTE_IN_SECONDS + random())


def fishing_content(hwnd, model):
    take_screenshot_and_crop(hwnd)
    predicted_number = get_number_from_model('/Fishing\\$screenshot.bmp', model)
    press_space_x_times(predicted_number)
    time.sleep(CONST_TIME_TO_RETRIEVE_FISH + random())
    random_f1_to_f4()
    press_space()
