import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

screen_width = 1200
screen_height = 790

def imageUploader():
    fileTypes = [("Image Files", "*.jpg *.jpeg *.png")]
    path = tk.filedialog.askopenfilename(filetypes=fileTypes)


    # if file is selected
    if len(path):
        img = Image.open(path)
        img_w, img_h = img.size
        if img_w <= screen_width and img_h <= screen_height:
            pic = ImageTk.PhotoImage(img)

        # Otherwise, resize proportionally to fit in screen
        img.thumbnail((screen_width, screen_height), Image.LANCZOS)
        pic = ImageTk.PhotoImage(img)

        app.geometry('1200x790')
        # clear canvas and redraw
        canvas.delete("all")
        canvas.create_image(600, 395, image=pic, anchor="center")
        canvas.image = pic  # keep a reference!

    # if no file is selected
    else:
        print('No file is selected')

if __name__ == '__main__':
    # definint tkinter object
    app = tk.Tk()
    # setting title and basic size to the app
    app.title("Image Watermarking Desktop App")
    app.geometry('1200x790')

    # add background image
    bg_img = Image.open("background.png")         # open image with PIL
    bg_img = bg_img.resize((screen_width, screen_height))
    img = ImageTk.PhotoImage(bg_img)

    canvas = tk.Canvas(app, width=screen_width, height=screen_height)
    canvas.pack()

    canvas.create_image(0, 0, image=img, anchor='nw')
    canvas.image = img

    # overlay text directly on canvas
    canvas.create_text(600, 100, text='Image Watermaking App',
                       font=('Arial', 25, 'bold'), fill='black')

    # define upload button
    uploadButton = tk.Button(app, text='Upload Image',
                             font=('Arial'), command=imageUploader)
    uploadButton.place(relx=0.5, rely=0.9, anchor='center')

    app.mainloop()