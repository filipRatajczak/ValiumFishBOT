import win32con
import win32gui
import win32ui


def create_background_screenshot(hwnd, width, height, file_name):
    create_screenshot_and_save_file(hwnd, height, width, file_name)


def delete_objects(compatible_device_context, data_bit_map, device_context_object, hwnd, window_device_context):
    device_context_object.DeleteDC()
    compatible_device_context.DeleteDC()
    win32gui.ReleaseDC(hwnd, window_device_context)
    win32gui.DeleteObject(data_bit_map.GetHandle())


def create_screenshot_and_save_file(hwnd, height, width, file_name):
    compatible_device_context, device_context_object, window_device_context = create_device_contexts(hwnd)
    data_bit_map = win32ui.CreateBitmap()
    data_bit_map.CreateCompatibleBitmap(device_context_object, width, height)
    compatible_device_context.SelectObject(data_bit_map)
    compatible_device_context.BitBlt((0, 0), (width, height), device_context_object, (0, 0), win32con.SRCCOPY)
    data_bit_map.SaveBitmapFile(compatible_device_context, f'${file_name}.bmp')
    delete_objects(compatible_device_context, data_bit_map, device_context_object, hwnd, window_device_context)


def create_device_contexts(hwnd):
    window_device_context = win32gui.GetWindowDC(hwnd)
    device_context_object = win32ui.CreateDCFromHandle(window_device_context)
    compatible_device_context = device_context_object.CreateCompatibleDC()
    return compatible_device_context, device_context_object, window_device_context
