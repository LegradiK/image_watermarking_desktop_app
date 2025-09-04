from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np


def get_position_coords(position, w, h):
    positions = {
        "top-left": (w * 0.1, h * 0.05),
        "top": (w / 2, h * 0.05),
        "top-right": (w * 0.87, h * 0.05),
        "left": (w * 0.1, h / 2),
        "center": (w / 2, h / 2),
        "right": (w * 0.87, h / 2),
        "bottom-left": (w * 0.1, h * 0.89),
        "bottom": (w / 2, h * 0.89),
        "bottom-right": (w * 0.87, h * 0.89)
    }
    return positionｓ.get(position.lower(), (w / 2, h / 2))

def get_anchor(position):
    left_positions = ['top-left', 'left', 'bottom-left']
    center_positions = ['top', 'center', 'bottom']
    right_positions = ['top-right', 'right', 'bottom-right']

    if position.lower() in left_positions:
        return 'la'
    elif position.lower() in center_positions:
        return 'ma'
    else:
        return 'ra'

def apply_watermark(image_path: str, watermark_text: str, font_path=None, font_size: int = None, position=None):
    # opening the file
    im = Image.open(image_path).convert('RGBA')

    # creating a new layer that will be on top of the picture
    # this is a transparent layer that will show watermarking texts
    text_layer = Image.new('RGBA', im.size, (255, 255, 255, 0))
    print(im.format, im.size, im.mode)

    # deciding the test_layer and font details
    draw = ImageDraw.Draw(text_layer)
    w, h = im.size

    if position is None:
        position = 'center'
    x, y = get_position_coords(position, w, h)
    anchor=get_anchor(position)

    if font_path is None:
        font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    if font_size is None:
        font_size = int(min(w, h) / 10)
    else:
        font_size = int(min(w, h) * font_size / 100)
    font = ImageFont.truetype(font_path, font_size)

    # text details
    draw.text((x, y), watermark_text, fill=(0, 0, 0, 50), font=font, anchor=anchor)

    # combining the text layer and picture
    watermarked = Image.alpha_composite(im, text_layer)

    plt.subplot(1, 2, 1)
    # converts the final PIL.Image to NumPy array so matplotlib can display
    plt.imshow(np.array(watermarked))
    # hide axis - as matplotlib automatically shows the axis ticks
    plt.axis('off')
    plt.show()