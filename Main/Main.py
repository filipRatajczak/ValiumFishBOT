import threading
import time

import Fishing.Fishing
from Client.MemoryReader import get_valium_process_object_details
from Fishing.Fishing import check_flag_stacked, go_fishing

# TODO DO OOP
# TODO GET MORE SCREENSHOTS AND DO BETTER MODEL

if __name__ == '__main__':
    handle = get_valium_process_object_details()
    stacked = threading.Thread(target=check_flag_stacked, args=(handle, 253,))
    idle = threading.Thread(target=check_flag_stacked, args=(handle, 1,))
    bot = threading.Thread(target=go_fishing, args=(handle,))
    bot.start()
    time.sleep(3 * Fishing.MINUTE_IN_SECONDS)
    stacked.start()
    idle.start()
