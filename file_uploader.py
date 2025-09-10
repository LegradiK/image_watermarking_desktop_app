import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from watermark import apply_watermark


class WatermarkApp:
    def __init__(self, root, watermark_text, font_size, position):
        self.root = root
        self.screen_width = 1200
        self.screen_height = 790
        self.watermark_text = watermark_text
        self.font_size = font_size
        self.position = position

        self.root.title("Image Watermarking Desktop App")
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')

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
        uploadButton = tk.Button(self.root, text='Upload Image',
                                font=('Arial'), command=self.imageUploader)
        uploadButton.place(relx=0.5, rely=0.9, anchor='center')


    def imageUploader(self):
        fileTypes = [("Image Files", "*.jpg *.jpeg *.png")]
        path = tk.filedialog.askopenfilename(filetypes=fileTypes)

        # if file is selected
        if len(path):
            img = Image.open(path)
            img_w, img_h = img.size
            if img_w > self.screen_width and img_h > self.screen_height:
                img.thumbnail((self.screen_width, self.screen_height), Image.LANCZOS)

            # Otherwise, resize proportionally to fit in screen
            pic = ImageTk.PhotoImage(img)

            # clear canvas and redraw
            self.canvas.delete("all")
            self.canvas.create_image(600, 395, image=pic, anchor="center")
            self.canvas.image = pic  # keep a reference!

        # if no file is selected
        else:
            print('No file is selected')

        # watermarking
        apply_watermark(
            image_path=path,
            watermark_text=self.watermark_text,
            font_size=self.font_size,
            position=self.position
        )

