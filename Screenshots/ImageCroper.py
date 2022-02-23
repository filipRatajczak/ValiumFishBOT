from PIL import Image


def crop_image(image_name):
    im = Image.open(f'${image_name}.bmp')
    cropped_image = im.crop((370, 430, 680, 510))
    cropped_image.save(f'${image_name}.bmp')
