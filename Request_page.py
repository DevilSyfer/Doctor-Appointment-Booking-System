from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import tkinter as tk
import sqlite3


def change_appointment(window, user_id):
    # Connect to the database
    with sqlite3.connect('appointment.db') as conn:
        cursor = conn.cursor()

    # Create a table for the appointments
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS appointment_request(id INTEGER PRIMARY KEY AUTOINCREMENT,Patient_name, '
        'doctor_name, appointment_time, appointment_date, appointment_id)')

    # Create the main window
    root = tk.Toplevel()
    root.title("Appointment Request")
    root.geometry("925x550+300+150")
    root.configure(bg="#fff")
    # root.grab_set()
    root.resizable(False, False)
    heading = tk.Label(root,
                       text='''Request for Appointment 
Changes''', bg='#fff', fg="#483D8B",
                       font=("Neue Metana Bold", 24, "bold"), justify='left')
    heading.place(x=500, y=50)

    # Open and resize the image using PIL (Pillow)
    img = Image.open(r"D:\Pycharm\project testing\images\update.png")
    resized_img = img.resize((500, 500), Image.ANTIALIAS)

    # Convert the resized image to a PhotoImage object
    photoimg = ImageTk.PhotoImage(resized_img)

    # Create a label for the image
    label1 = tk.Label(root, image=photoimg, border=0)
    label1.place(x=0, y=0)
    label1.image = photoimg

    # Create patient name label and entry
    cursor.execute("select username from users where id=?", (user_id,))
    user_name = cursor.fetchone()[0]
    patient_name_label = tk.Label(root, text='Patient Name:', bg='#fff')
    patient_name_label.place(x=500, y=150)
    user_name_var = tk.StringVar(value=user_name)
    patient_name_entry = tk.Entry(root, textvariable=user_name_var, state='readonly')
    patient_name_entry.place(x=630, y=150)

    # Get all appointment IDs from the database
    cursor.execute("SELECT appointment_id FROM appointment")
    appointments = [row[0] for row in cursor.fetchall()]

    # Create Appointment ID label and dropdown menu
    appointment_label = tk.Label(root, text='Appointment ID:', bg='#fff')
    appointment_label.place(x=500, y=200)
    appointment_var = tk.StringVar(root)
    appointment_var.set(appointments[0])
    appointment_dropdown = tk.OptionMenu(root, appointment_var, *appointments)
    appointment_dropdown.place(x=630, y=200)

    # Fetch the specializations from the database
    cursor.execute("SELECT DISTINCT specialization FROM doctors")
    specializations = [row[0] for row in cursor.fetchall()]

    # Create the specialization label and dropdown
    specialization_label = tk.Label(root, text="Select a specialization:", bg='#fff')
    specialization_label.place(x=500, y=250)

    specialization_var = tk.StringVar(root)
    specialization_var.set(specializations[0])
    specialization_dropdown = tk.OptionMenu(root, specialization_var, *specializations)
    specialization_dropdown.place(x=630, y=250)

    # Create name label and entry
    # Create the doctor label and dropdown
    doctor_label = tk.Label(root, text="Select a doctor:", bg='#fff')
    doctor_label.place(x=500, y=300)
    doctors_var = tk.StringVar(root)
    doctors = []
    cursor.execute("SELECT name FROM doctors WHERE specialization = ?", (specialization_var.get(),))
    for row in cursor.fetchall():
        doctors.append(row[0])
    doctors_var.set(doctors[0])
    doctor_dropdown = tk.OptionMenu(root, doctors_var, *doctors)
    doctor_dropdown.place(x=630, y=300)

    # Create date label and entry
    today = datetime.today().date()
    date_label = tk.Label(root, text="Select an date:", bg='#fff')
    date_label.place(x=500, y=350)
    date_entry = DateEntry(root, width=12, background='dark-blue',
                           foreground='white', borderwidth=2, year=2023, pady=10, mindate=today)
    date_entry.place(x=630, y=350)

    # Function to update the doctor dropdown based on the selected specialization
    def update_doctors(*args):
        doctors.clear()
        cursor.execute("SELECT name FROM doctors WHERE specialization = ?", (specialization_var.get(),))
        for row in cursor.fetchall():
            doctors.append(row[0])
        doctors_var.set(doctors[0])
        menu = doctor_dropdown["menu"]
        menu.delete(0, "end")
        for doctor in doctors:
            menu.add_command(label=doctor, command=(doctors_var, doctor))

    # Bind the update_doctors function to the specialization dropdown
    specialization_var.trace('w', update_doctors)
    # Create time label and entry
    time_label = tk.Label(root, text="Select a time:", bg='#fff')
    time_label.place(x=500, y=400)
    times = ["10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
    time_var = tk.StringVar(root)
    time_var.set(times[0])
    time_dropdown = tk.OptionMenu(root, time_var, *times)
    time_dropdown.place(x=630, y=400)

    # Create submit button
    def submit_request():
        # Get the values from the entries
        patient_name = patient_name_entry.get()
        appointment_id = appointment_var.get()
        doctor = doctors_var.get()
        date = date_entry.get()
        time = time_var.get()
        cursor.execute("select appointment_id from appointment")
        appointment_ids = [row[0] for row in cursor.fetchall()]
        if not doctor.isalpha():
            tk.messagebox.showerror("Error", "Doctor name must Alphabet ")
        elif doctor == "":
            tk.messagebox.showerror("Error", "Doctor name not be empty ")
        elif not patient_name.isalpha():
            tk.messagebox.showerror("Error", "Doctor name must Alphabet ")
        elif patient_name == "":
            tk.messagebox.showerror("Error", "Doctor name not be empty ")
        elif appointment_id not in appointment_ids:
            tk.messagebox.showerror("Error", "Appointment id is not Correct")
        else:
            # Insert the new appointment request into the database
            cursor.execute(
                "INSERT INTO appointment_request(Patient_name,"
                "appointment_id, doctor_name,appointment_date, appointment_time) VALUES (?, "      
                "?, ?, ?, ?)", (patient_name, appointment_id, doctor, date, time))
            conn.commit()
            # Show a message box confirming the submission
            tk.messagebox.showinfo("Request Submitted", "Your appointment request has been submitted.")

    submit_button = tk.Button(root, text="Submit", command=submit_request)
    submit_button.place(x=580, y=480)

    # Run the program
    root.mainloop()
