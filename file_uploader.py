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
        pic = ImageTk.PhotoImage(img)

        app.geometry('560x300')
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
    imgLabel = Label(app, image=img)
    imgLabel.place(x=0, y=0)

    #add background color to upload button
    app.option_add('*Label*Background', 'white')
    app.option_add('*Button*Background', 'white')

    label = tk.Label(app)
    label.pack(pady=10)

    # define upload button
    uploadButton = tk.Button(app, text='Upload Image', command=imageUploader)
    uploadButton.pack(side=tk.BOTTOM, pady=20)

    app.mainloop()