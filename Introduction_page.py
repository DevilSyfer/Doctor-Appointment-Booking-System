import tkinter as tk
from PIL import ImageTk
from PIL import Image
from login import Login


def introduction():
    window = tk.Tk()
    window.title("Signin")
    window.geometry("1520x785+0+0")
    window.configure(bg="#6260C2")
    heading = tk.Label(window,
                       text='''Appointment
Booking''', bg='#6260C2', fg='#FC740C',
                       font=("Bell MT", 44, "bold"), justify='left')
    heading.place(x=120, y=200)

    # Introduction
    intro = tk.Label(window,
                     text='''Welcome to our appointment booking system. 
Our platform provides an easy and efficient 
way to book appointments with your preferred 
service provider. With just a few clicks, 
you can schedule your appointment and receive 
confirmation, making the process hassle-free.''', bg='#6260C2', fg='#fff',
                     font=("Neue Metana Bold", 12, "bold"), justify='left')
    intro.place(x=120, y=350)

    img1 = tk.PhotoImage(file=r"D:\Pycharm\project testing\images\healthcare.png")
    tk.Label(image=img1, bg="#6260C2").place(x=20, y=20)

    def destroy_introduction():
        window.destroy()

    # Open and resize intro2 image
    img = Image.open(r"D:\Pycharm\project testing\images\intro2.png")
    resized_img = img.resize((800, 500), Image.ANTIALIAS)
    photoimg = ImageTk.PhotoImage(resized_img)

    # Create label for intro2 image
    label1 = tk.Label(window, image=photoimg, border=0)
    label1.place(x=700, y=185)

    # Open and resize intro3 image
    img3 = Image.open(r"D:\Pycharm\project testing\images\more.png")
    resized_img3 = img3.resize((200, 200), Image.ANTIALIAS)
    photoimg3 = ImageTk.PhotoImage(img3)

    button = tk.Button(window, image=photoimg3, border=0, bg="#6260C2", cursor="hand2")
    button.place(x=120, y=500)

    # Open and resize intro3 image
    img4 = Image.open(r"D:\Pycharm\project testing\images\sign3.jpeg")
    resized_img4 = img4.resize((200, 200), Image.ANTIALIAS)
    photoimg4 = ImageTk.PhotoImage(img4)

    button = tk.Button(window, image=photoimg4, border=0, bg="#6260C2",
                       command=lambda: [destroy_introduction(),Login()], cursor="hand2")
    button.place(x=1250, y=20)

    window.mainloop()

introduction()
# if __name__ == "__main__":
#     introduction()
