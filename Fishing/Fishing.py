import logging
import time
from random import random

import tensorflow
import win32gui

from AI.DigitRecognizer import DigitRecognizer
from Client.Clicker import press_random_f1_to_f4, press_space, press_space_x_times
from Client.MemoryReader import MemoryReader
from Screen.Screenshoter import Screenshooter


class Fishing:
    hwnd = win32gui.FindWindow(None, "Valium.pl")
    model = tensorflow.keras.models.load_model('digit_recognizer.h5')
    SPACE = 0x39
    F1 = 0x3B
    F4 = 0X3E
    CONST_TIME_TO_RETRIEVE_FISH = 8
    MINUTE_IN_SECONDS = 60
    DEFAULT_SCREENSHOT_NAME = 'screenshot'
    DEFAULT_SCREENSHOT_NAME_WITH_EXTENSION = 'screenshot.bmp'
    IDLE_FLAG = 253
    FISH_FLAG = 1

    def __init__(self):
        self.__screenshooter__ = Screenshooter()
        self.__digit_recognizer__ = DigitRecognizer()
        self.__memory_reader__ = MemoryReader()
        self.__handle__ = self.__memory_reader__.get_valium_process_object_details()

    @staticmethod
    def initial_fishing():
        press_random_f1_to_f4()
        time.sleep(random() / 2)
        press_space()

    def fishing(self):
        logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info(f'VALIUM FISH-BOT STARTED')
        self.initial_fishing()

        counter = 0

        while True:
            isFish = self.__memory_reader__.get_fishing_flag(self.__handle__)
            time.sleep(random())
            if isFish == self.FISH_FLAG:
                logging.info(f'FLAG IS SET TO {self.FISH_FLAG}')
                self.fishing_content(self)
                counter = counter + 1

    @staticmethod
    def fishing_content(self):
        self.__screenshooter__.take_screenshot_and_crop(self.DEFAULT_SCREENSHOT_NAME)
        predicted_number = self.__digit_recognizer__.get_number_from_model(self.DEFAULT_SCREENSHOT_NAME_WITH_EXTENSION,
                                                                           self.model)
        self.__screenshooter__.set_focus_on_window()
        press_space_x_times(predicted_number)
        time.sleep(self.CONST_TIME_TO_RETRIEVE_FISH + random())
        press_random_f1_to_f4()
        press_space()

    def check_flag_stacked(self):
        while True:
            isFish = self.__memory_reader__.get_fishing_flag(self.__handle__)
            if isFish == self.FISH_FLAG:
                time.sleep(random())
                start_time = time.time()
                self.check_idle(isFish, start_time)

    def check_idle(self, isFish, start_time):
        while isFish == self.FISH_FLAG:
            isFish = self.__memory_reader__.get_fishing_flag(self.__handle__)
            time.sleep(3)
            stop_time = time.time()
            total_time = stop_time - start_time
            if total_time > self.MINUTE_IN_SECONDS:
                logging.warning(
                    f'FISH-BOT GOT STACKED WHEN FLAG = {isFish} FOR {total_time} SECONDS, TRYING TO REPAIR IT...')
                self.__screenshooter__.set_focus_on_window()
                self.initial_fishing()
                time.sleep(self.MINUTE_IN_SECONDS + random())
