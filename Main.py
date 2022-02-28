from Fishing.Fishing import Fishing
from threading import Thread

FISH_FLAG = 1
IDLE_FLAG = 253

if __name__ == '__main__':
    fishing = Fishing()
    stacked = Thread(target=fishing.check_flag_stacked, args=(IDLE_FLAG,))
    idle = Thread(target=fishing.check_flag_stacked, args=(FISH_FLAG,))
    bot = Thread(target=fishing.fishing, args=())
    bot.start()
    stacked.start()
    idle.start()
