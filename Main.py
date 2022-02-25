from Fishing.Fishing import Fishing
from threading import Thread

if __name__ == '__main__':
    fishing = Fishing()
    stacked = Thread(target=fishing.check_flag_stacked, args=())
    idle = Thread(target=fishing.check_flag_stacked, args=())
    bot = Thread(target=fishing.fishing, args=())
    bot.start()
    stacked.start()
    idle.start()
