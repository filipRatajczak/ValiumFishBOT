import pymem
import pymem.process
import pymem.memory

OFFSET = 0x2AE5D7C


class MemoryReader:

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_valium_process_object_details():
        return pymem.Pymem("valium.exe")

    @staticmethod
    def get_fishing_flag(valium_object):
        mem = pymem.memory
        handle = valium_object.process_handle
        address = valium_object.base_address + OFFSET
        return mem.read_short(handle, address)
