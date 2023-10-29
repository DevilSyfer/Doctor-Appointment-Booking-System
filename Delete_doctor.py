from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import messagebox
from PIL import ImageTk, Image


def delete_doctor():
    def Delete_doctor():
        doctor_ID = doctor_var.get()

        with sqlite3.connect('appointment.db') as conn:
            c = conn.cursor()
            c.execute("DELETE FROM doctors WHERE id=?", (doctor_ID,))
            conn.commit()

        messagebox.showinfo("Deletion", "Doctor deleted successfully")

        # Clear the entry fields
        specialization_var.set("")
        doctor_name_var.set("")

        # Refresh the window
        refresh_window()

    def update_doctor_details(*args):
        doctor_ID = doctor_var.get()

        with sqlite3.connect('appointment.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM doctors WHERE id=?", (doctor_ID,))
            doctor_detail = c.fetchone()

            if doctor_detail:
                specialization_var.set(doctor_detail[1])
                doctor_name_var.set(doctor_detail[2])

    def refresh_window():
        doctor_dropdown['menu'].delete(0, END)

        with sqlite3.connect('appointment.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM doctors")
            doctor_id = [row[0] for row in c.fetchall()]

            if doctor_id:
                doctor_var.set(doctor_id[0])
            else:
                doctor_var.set('')

            for id in doctor_id:
                doctor_dropdown['menu'].add_command(label=id, command=tk._setit(doctor_var, id))

    root = Toplevel()
    root.geometry("700x400+400+200")
    root.title('Delete Doctor')
    root.configure(bg="#F3F3F3")
    root.grab_set()

    heading = tk.Label(root,
                       text='''Doctor
Deactivation''', bg='#F3F3F3', fg="#483D8B",
                       font=("Bell MT", 28, "bold"), justify='left')
    heading.place(x=400, y=70)

    # Open and resize the image using PIL (Pillow)
    img = Image.open(r"D:\Pycharm\project testing\images\delete.png")
    resized_img = img.resize((400, 400), Image.ANTIALIAS)

    # Convert the resized image to a PhotoImage object
    photoimg = ImageTk.PhotoImage(resized_img)

    # Create a label for the image
    label1 = tk.Label(root, image=photoimg, border=0)
    label1.place(x=0, y=0)
    label1.image = photoimg

    with sqlite3.connect('appointment.db') as conn:
        c = conn.cursor()

        c.execute("SELECT id FROM doctors")
        doctor_id = [row[0] for row in c.fetchall()]

        doctor_var = tk.StringVar(root)
        if doctor_id:
            doctor_var.set(doctor_id[0])
        else:
            doctor_var.set('')
        doctor_label = tk.Label(root, text="Doctor ID:")
        doctor_label.place(x=400, y=200)

        doctor_dropdown = tk.OptionMenu(root, doctor_var, *doctor_id)
        doctor_dropdown.place(x=520, y=200)

    specialization_label = tk.Label(root, text="Doctor Specialization:")
    specialization_label.place(x=400, y=240)
    specialization_var = tk.StringVar(value="")
    specialization_entry = tk.Entry(root, textvariable=specialization_var, state="readonly")
    specialization_entry.place(x=520, y=240)

    doctor_name_label = tk.Label(root, text="Doctor Name:")
    doctor_name_label.place(x=400, y=280)
    doctor_name_var = tk.StringVar(value='')
    doctor_name_entry = tk.Entry(root, textvariable=doctor_name_var, state="readonly")
    doctor_name_entry.place(x=520, y=280)

    doctor_var.trace('w', update_doctor_details)

    delete_button = Button(root, text='Delete', command=Delete_doctor)
    delete_button.place(x=490, y=330)

    root.mainloop()
