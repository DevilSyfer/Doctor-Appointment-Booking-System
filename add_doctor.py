import tkinter as tk
import sqlite3
from tkinter import messagebox
from PIL import ImageTk, Image


def Add_Doctors():
    # create database connection and cursor
    with sqlite3.connect('appointment.db') as conn:
        c = conn.cursor()

    # create the doctors table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY,
                name TEXT,
                specialization TEXT
                )''')

    # function to add a new doctor to the database
    def add_doctor():
        # get the values entered by the user
        names = name_entry.get()
        specialization = specialization_entry.get()

        if not all(name.isalpha() or name.isspace() for name in names):
            tk.messagebox.showerror("Error", "Doctor name must be Alphabetic.")
            return
        elif not all(name.isalpha() or name.isspace() for name in specialization):
            tk.messagebox.showerror("Error", "Doctor specialization must be Alphbetic.")
            root.grab_set()
            return
        else:
            # insert the new doctor into the database
            c.execute("INSERT INTO doctors (name, specialization) VALUES (?, ?)",
                      (names, specialization))

        # commit the changes to the database
        conn.commit()

        # clear the entry fields
        name_entry.delete(0, tk.END)
        specialization_entry.delete(0, tk.END)

    # create the tkinter window and widgets
    root = tk.Toplevel()
    root.geometry("700x400+400+200")
    root.title('Add Doctor')
    root.configure(bg='#fff')

    heading = tk.Label(root,
                       text='''Growing
the Team''', bg='#fff', fg="#483D8B",
                       font=("Bell MT", 28, "bold"), justify='left')
    heading.place(x=400, y=70)

    # Open and resize the image using PIL (Pillow)
    img = Image.open(r"D:\Pycharm\project testing\images\doctor.png")
    resized_img = img.resize((400, 400), Image.ANTIALIAS)

    # Convert the resized image to a PhotoImage object
    photoimg = ImageTk.PhotoImage(resized_img)

    # Create a label for the image
    label1 = tk.Label(root, image=photoimg, border=0)
    label1.place(x=0, y=0)
    label1.image = photoimg

    name_label = tk.Label(root, text='Doctor Name:', bg="#fff")
    name_label.place(x=400, y=180)

    name_entry = tk.Entry(root)
    name_entry.place(x=530, y=180)

    specialization_label = tk.Label(root, text=' Doctor Specialization:', bg="#fff")
    specialization_label.place(x=400, y=210)

    specialization_entry = tk.Entry(root)
    specialization_entry.place(x=530, y=210)

    add_button = tk.Button(root, text='Add Doctor', command=add_doctor)
    add_button.place(x=500, y=250)

    root.mainloop()
