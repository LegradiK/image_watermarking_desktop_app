import tkinter as tk
from tkinter import Label
from tkinter import filedialog
from PIL import Image, ImageTk


def imageUploader():
    fileTypes = [('Image files', '*.png;*.jpg;*.jpeg')]
    path = tk.filedialog.askopenfilename(filetypes=fileTypes)

    # if file is selected
    if len(path):
        img = Image.open(path)
        uploaded_img = uploaded_img.resize((600, 350))
        pic = ImageTk.PhotoImage(img)

        app.geometry('600x350')
        label.config(image=pic)
        label.image = pic
    # if no file is selected
    else:
        print('No file is selected')

if __name__ == '__main__':
    # definint tkinter object
    app = tk.Tk()
    # setting title and basic size to the app
    app.title("Image Watermarking Desktop App")
    app.geometry('600x350')

    # add background image
    bg_img = Image.open("background.png")         # open image with PIL
    bg_img = bg_img.resize((600, 350))
    img = ImageTk.PhotoImage(bg_img)

    canvas = tk.Canvas(app, width=600, height=350)
    canvas.pack()

    canvas.create_image(0, 0, image=img, anchor='nw')
    canvas.image = img

    # overlay text directly on canvas
    canvas.create_text(300, 50, text='Image Watermaking App',
                       font=('Arial', 25, 'bold'), fill='darkgrey')

    # define upload button
    uploadButton = tk.Button(app, text='Upload Image',
                             font=('Arial'), command=imageUploader)
    uploadButton.pack(side=tk.BOTTOM, pady=30)

    app.mainloop()