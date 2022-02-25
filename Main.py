import time

from Client.MemoryReader import get_valium_process_object_details
from Fishing.Fishing import check_flag_stacked, fishing
from threading import Thread

IDLE_FLAG = 253
STACKED_FLAG = 1

if __name__ == '__main__':
    handle = get_valium_process_object_details()
    # stacked = Thread(target=check_flag_stacked, args=(handle, IDLE_FLAG,))
    # idle = Thread(target=check_flag_stacked, args=(handle, STACKED_FLAG,))
    bot = Thread(target=fishing, args=(handle, STACKED_FLAG,))
    bot.start()
    # time.sleep(2)
    # stacked.start()
    # idle.start()
