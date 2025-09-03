from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image as img
from matplotlib import pyplot as plt
import numpy as np

im = img.open('Lego Star Wars Winter.jpg')
print(im.format, im.size, im.mode)

im.show()
plt.imshow(im)