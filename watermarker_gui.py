import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from tkinter import colorchooser
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFont, ImageDraw, ImageColor
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
        self.watermarked_img = None
        self.font_color = None

        self.root.title("Image Watermarking Desktop App")
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')

        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Upload Image', command=self.imageUploader)
        self.filemenu.add_command(label='Watermarking', command=self.waterMarker)
        self.filemenu.add_command(label="Save", command=self.save, accelerator="Ctrl+S")
        self.filemenu.add_command(label="Save as...", command=self.save_as, accelerator="Ctrl+Shift+S")
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=root.quit)
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.helpmenu)
        self.helpmenu.add_command(label='About', command=self.open_about)

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
        watermarker_window.geometry('300x400')

        tk.Label(watermarker_window, text='Watermark Text:').pack(pady=5)
        text_var = StringVar()
        tk.Entry(watermarker_window, textvariable=text_var).pack(pady=5)

        tk.Label(watermarker_window, text='Font Size (% of image):').pack(pady=5)
        size_var = StringVar(value='10')
        tk.Entry(watermarker_window, textvariable=size_var).pack(pady=5)

        tk.Label(watermarker_window, text='Font:').pack(pady=5)
        font_var = StringVar(value="DejaVuSans")
        fonts = sorted(set(tkFont.families()))  # get system fonts
        OptionMenu(watermarker_window, font_var, *fonts).pack(pady=5)

        def pick_color():
            chosen_color = colorchooser.askcolor(title="Pick Watermark Colour")
            if chosen_color[1]:  # hex colour
                color_var.set(chosen_color[1])
                color_btn.config(
                                text=color_var.get(),
                                bg=color_var.get(),
                                fg='black' if chosen_color[1].lower() != "#ffffff" else "black"
                                )
        tk.Label(watermarker_window, text='Font Colour:').pack(pady=5)
        color_var = StringVar(value="#000000")  # default black
        color_btn = tk.Button(
            watermarker_window,
            text=color_var.get(),
            command=pick_color,
            bg=color_var.get(),
            fg='white'
            )
        color_btn.pack(pady=5)


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
            self.font_family = font_var.get()
            self.position = position_var.get()
            self.font_color = color_var.get()

            if not self.text:
                    messagebox.showwarning("No text", "Please enter watermark text.")
                    return
            try:
                self.font_size = int(self.font_size)
            except ValueError:
                self.font_size = None

            watermarked = self.apply_watermark(
                self.image_path,
                self.text,
                self.font_size,
                self.font_family,
                self.position,
                self.font_color
                )

            self.watermarked_img = watermarked

            display_img = watermarked.copy()
            display_img.thumbnail((self.screen_width, self.screen_height), Image.LANCZOS)

            tk_img = ImageTk.PhotoImage(display_img)
            self.canvas.delete('all')
            self.canvas.create_image(600, 395, image=tk_img, anchor='center')
            self.canvas.image = tk_img

            watermarker_window.destroy()

        tk.Button(watermarker_window, text='Apply', command=apply_and_show).pack(pady=15)

    def apply_watermark(self, image_path, text, font_size, font_family, position='center', font_color="#000000"):
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


        if font_size is None:
            font_size = int(min(im_w, im_h) / 10)
        else:
            font_size = int(min(im_w, im_h) * font_size / 100)

        try:
            font = ImageFont.truetype(f'{font_family}.ttf', font_size)
        except:
            font = ImageFont.load_default()

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
        x, y = positions.get(position.lower(), (im_w / 2, im_h / 2))

        left_positions = ['top-left', 'left', 'bottom-left']
        center_positions = ['top', 'center', 'bottom']

        if position.lower() in left_positions:
            anchor = 'la'
        elif position.lower() in center_positions:
            anchor =  'ma'
        else:
            anchor =  'ra'

        rgba_color = ImageColor.getrgb(font_color) + (100,) # add transparency
        draw.text((x, y), text=text, fill=rgba_color, font=font, anchor=anchor)
        # print(im.size)
        # print(text_layer.size)

        return Image.alpha_composite(im, text_layer)


    def save(self):
        if self.watermarked_img is None:
            messagebox.showwarning("No image", "Please apply a watermark before saving.")
            return

        try:
            # Save to the last chosen filename
            self.watermarked_img.save(self.f)
            messagebox.showinfo("Saved", f"Image saved to {self.f}")
        except AttributeError:
            # If no filename exists yet → ask user
            self.save_as()

    def save_as(self):
        if self.watermarked_img is None:
                    messagebox.showwarning("No image", "Please apply a watermark before saving.")
                    return

        f = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg;*.jpeg"),
                ("All Files", "*.*"),
            ]
        )
        if f:
            self.watermarked_img.save(f)
            self.f = f
            messagebox.showinfo("Saved", f"Image saved to {f}")

    def open_about(self):
        """Open 'About' popup page to show copyright"""
        about = tk.Toplevel(self.root)  # use self.root as parent
        about.title('About')
        about.geometry('400x250')
        about.resizable(False, False)

        label = tk.Label(
            about,
            text='Image Watermarking App\n\n'
                'Created with Python and Tkinter\n'
                'Copyright 2025 LegradiK',
            font=('Arial', 16),
            justify='center'
        )
        label.pack(expand=True, padx=20, pady=20)

        close_button = tk.Button(
            about,
            text='Close',
            command=about.destroy
        )
        close_button.pack(pady=10)
