import tkinter as tk
from file_uploader import WatermarkApp

# terminal inputs
watermark_text = input('Enter the watermark text to personalise your image: ')
font_size = input('Enter font size as a percentage of the image size (default 10%): ')

if font_size == '':
    font_size = None
else:
    try:
        font_size = int(font_size)
    except ValueError:
        print('Invalid font size entered. Using automatic sizing.')
        font_size = None

position = input("Enter watermark position (top-left, top, top-right, left, center, right, bottom-left, bottom, bottom-right) [default: center]: ").strip()
if position == '':
    position = None
else:
    position = position

# GUI
root = tk.Tk()
app = WatermarkApp(root, watermark_text, font_size, position)
root.mainloop()

