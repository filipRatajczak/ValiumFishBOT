import win32api
import win32con
import win32gui
import win32process
import win32ui
from PIL import Image


class Screenshooter:

    def __init__(self):
        self.hwnd = win32gui.FindWindow(None, "Valium.pl")

    @staticmethod
    def load_image(path):
        Image.init()
        return Image.open(path)

    def create_background_screenshot(self, width, height, file_name):
        self.create_screenshot_and_save_file(height, width, file_name)

    def delete_objects(self, compatible_device_context, data_bit_map, device_context_object,
                       window_device_context):
        device_context_object.DeleteDC()
        compatible_device_context.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, window_device_context)
        win32gui.DeleteObject(data_bit_map.GetHandle())

    def create_screenshot_and_save_file(self, height, width, file_name):
        compatible_device_context, device_context_object, window_device_context = self.create_device_contexts()
        data_bit_map = win32ui.CreateBitmap()
        data_bit_map.CreateCompatibleBitmap(device_context_object, width, height)
        compatible_device_context.SelectObject(data_bit_map)
        compatible_device_context.BitBlt((0, 0), (width, height), device_context_object, (0, 0), win32con.SRCCOPY)
        data_bit_map.SaveBitmapFile(compatible_device_context, f'{file_name}.bmp')
        self.delete_objects(compatible_device_context, data_bit_map, device_context_object, window_device_context)

    def create_device_contexts(self):
        window_device_context = win32gui.GetWindowDC(self.hwnd)
        device_context_object = win32ui.CreateDCFromHandle(window_device_context)
        compatible_device_context = device_context_object.CreateCompatibleDC()
        return compatible_device_context, device_context_object, window_device_context

    def take_screenshot_and_crop(self, file_name):
        self.create_background_screenshot(680, 510, file_name)
        self.crop_image(file_name)

    @staticmethod
    def crop_image(image_name):
        im = Image.open(f'{image_name}.bmp')
        cropped_image = im.crop((370, 430, 680, 510))
        cropped_image.save(f'{image_name}.bmp')

    def set_focus_on_window(self):
        remote_thread, _ = win32process.GetWindowThreadProcessId(self.hwnd)
        win32process.AttachThreadInput(win32api.GetCurrentThreadId(), remote_thread, True)
        win32gui.SetFocus(self.hwnd)
