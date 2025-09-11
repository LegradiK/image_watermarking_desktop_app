import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFont, ImageDraw
from matplotlib import pyplot as plt
import numpy as np


class WaterMarkerApp():
    def __init__(self, root):
        self.root = root
        self.screen_width = 1200
        self.screen_height = 790
        self.image_path = None
        self.img = None
        self.text = None
        self.font_size = None
        self.position = None

        self.root.title("Image Watermarking Desktop App")
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')

        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Upload Image', command=self.imageUploader)
        self.filemenu.add_command(label='Watermarking', command=self.waterMarker)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=root.quit)
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.helpmenu)
        self.helpmenu.add_command(label='About')

        # add background image
        bg_img = Image.open("background.png")         # open image with PIL
        bg_img = bg_img.resize((self.screen_width, self.screen_height))
        self.img = ImageTk.PhotoImage(bg_img)

        self.canvas = tk.Canvas(root, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()

        self.canvas.create_image(0, 0, image=self.img, anchor='nw')
        self.canvas.image = self.img

        # overlay text directly on canvas
        self.canvas.create_text(600, 100, text='Image Watermaking App',
                        font=('Arial', 25, 'bold'), fill='black')

        # define upload button
        # uploadButton = tk.Button(self.root, text='Upload Image',
        #                         font=('Arial'), command=self.imageUploader)
        # uploadButton.place(relx=0.5, rely=0.9, anchor='center')


    def imageUploader(self):
        fileTypes = [("Image Files", "*.jpg *.jpeg *.png")]
        path = tk.filedialog.askopenfilename(filetypes=fileTypes)

        # if file is selected
        if len(path):
            self.image_path = path
            self.img = Image.open(path)
            img_w, img_h = self.img.size
            # print(self.img.size)
            if img_w > self.screen_width and img_h > self.screen_height:
                self.img.thumbnail((self.screen_width, self.screen_height), Image.LANCZOS)

            # Otherwise, resize proportionally to fit in screen
            pic = ImageTk.PhotoImage(self.img)

            # clear canvas and redraw
            self.canvas.delete("all")
            self.canvas.create_image(600, 395, image=pic, anchor="center")
            self.canvas.image = pic  # keep a reference!

        # if no file is selected
        else:
            print('No file is selected')


    def waterMarker(self):
        if not self.image_path:
            messagebox.showwarning('No image', 'Please upload an image.')
            return

        watermarker_window = Toplevel(self.root)
        watermarker_window.title('Add Watermark')
        watermarker_window.geometry('300x250')

        tk.Label(watermarker_window, text='Watermark Text:').pack(pady=5)
        text_var = StringVar()
        tk.Entry(watermarker_window, textvariable=text_var).pack(pady=5)

        tk.Label(watermarker_window, text='Font Size (% of image):').pack(pady=5)
        size_var = StringVar(value='10')
        tk.Entry(watermarker_window, textvariable=size_var).pack(pady=5)

        tk.Label(watermarker_window, text='Position:').pack(pady=5)
        position_var = StringVar(value='center')
        positions = [
            'top-left', 'left', 'bottom-left',
            'top', 'center', 'bottom', 'top-right',
            'right', 'bottom-right'
        ]
        OptionMenu(watermarker_window, position_var, *positions).pack(pady=5)

        def apply_and_show():
            self.text = text_var.get()
            self.font_size = size_var.get()
            self.position = position_var.get()

            if not self.text:
                    messagebox.showwarning("No text", "Please enter watermark text.")
                    return
            try:
                self.font_size = int(self.font_size)
            except ValueError:
                self.font_size = None

            watermarked = self.apply_watermark(self.image_path, self.text, self.font_size, self.position)

            display_img = watermarked.copy()
            display_img.thumbnail((self.screen_width, self.screen_height), Image.LANCZOS)

            tk_img = ImageTk.PhotoImage(display_img)
            self.canvas.delete('all')
            self.canvas.create_image(600, 395, image=tk_img, anchor='center')
            self.canvas.image = tk_img

            watermarker_window.destroy()

        tk.Button(watermarker_window, text='Apply', command=apply_and_show).pack(pady=15)

    def apply_watermark(self, image_path, text, font_size, position):
        # opening the file
        im = Image.open(image_path).convert('RGBA')
        im_w, im_h = im.size

        # if im_w > self.screen_width and im_h > self.screen_height:
        #         im.thumbnail((self.screen_width, self.screen_height), Image.LANCZOS)

        # creating a new layer that will be on top of the picture
        # this is a transparent layer that will show watermarking texts
        text_layer = Image.new('RGBA', im.size, (255, 255, 255, 0))
        # print(im.format, im.size, im.mode)

        # deciding the test_layer and font details
        draw = ImageDraw.Draw(text_layer)

        font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

        if font_size is None:
            font_size = int(min(im_w, im_h) / 10)
        else:
            font_size = int(min(im_w, im_h) * font_size / 100)
        font = ImageFont.truetype(font_path, font_size)

        positions = {
            "top-left": (im_w * 0.1, im_h * 0.05),
            "top": (im_w / 2, im_h * 0.05),
            "top-right": (im_w * 0.87, im_h * 0.05),
            "left": (im_w * 0.1, im_h / 2),
            "center": (im_w / 2, im_h / 2),
            "right": (im_w * 0.87, im_h / 2),
            "bottom-left": (im_w * 0.1, im_h * 0.89),
            "bottom": (im_w / 2, im_h * 0.89),
            "bottom-right": (im_w * 0.87, im_h * 0.89)
        }
        x, y = positionｓ.get(position.lower(), (im_w / 2, im_h / 2))

        left_positions = ['top-left', 'left', 'bottom-left']
        center_positions = ['top', 'center', 'bottom']

        if position.lower() in left_positions:
            anchor = 'la'
        elif position.lower() in center_positions:
            anchor =  'ma'
        else:
            anchor =  'ra'

        draw.text((x, y), text=text, fill=(0, 0, 0, 100), font=font, anchor=anchor)
        # print(im.size)
        # print(text_layer.size)
        return Image.alpha_composite(im, text_layer)

