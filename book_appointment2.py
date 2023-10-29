import tkinter as tk
import string
import random
import sqlite3
from tkcalendar import DateEntry
from tkinter import messagebox
import datetime


def Book_Appointment(window, user_id):
    # Generate random appointment ID
    def generate_appointment_id():
        appointment_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return appointment_id

    # Connect to database
    with sqlite3.connect('appointment.db') as conn:
        c = conn.cursor()

        # Create appointments table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS appointment
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   customer_name text,
                   patient_name TEXT,
                   doctor_name TEXT,
                   specialization text,
                   appointment_time TEXT,
                   appointment_date TEXT,
                   appointment_id TEXT,                
                   user_id text)''')
    conn.commit()

    # Create tkinter window
    window = tk.Toplevel()
    window.title('Book Appointment')
    window.geometry("925x600+300+160")
    window.configure(bg="#fff")

    heading = tk.Label(window,
                       text='''EASY
BOOKING''', bg='#fff', fg="#483D8B",
                       font=("Neue Metana Bold", 32, "bold"), justify='left')
    heading.place(x=500, y=50)

    img1 = tk.PhotoImage(file=r"D:\Pycharm\project testing\images\booking_logo.png")
    tk.Label(window, image=img1, border=0, bg="white").place(x=50, y=10)

    img2 = tk.PhotoImage(file=r"D:\Pycharm\project testing\images\booking.png")
    tk.Label(window, image=img2, border=0, bg="white").place(x=50, y=150)

    root = tk.Frame(window, width=400, height=400, bg="#fff")
    root.place(x=500, y=150)

    appointment_id_label = tk.Label(root, text='Appointment ID:', bg="#fff")
    appointment_id_label.place(x=10, y=10)
    appointment_id_var = tk.StringVar()
    appointment_id = generate_appointment_id()
    appointment_id_var.set(appointment_id)
    appointment_id_entry = tk.Entry(root, textvariable=appointment_id_var, state='readonly')
    appointment_id_entry.place(x=170, y=10)

    # Create patient name label and entry
    c.execute("select username from users where id=?", (user_id,))
    user_name = c.fetchone()[0]
    customer_name_label = tk.Label(root, text='Customer Name:', bg="#fff")
    customer_name_label.place(x=10, y=50)
    user_name_var = tk.StringVar(value=user_name)
    customer_name_entry = tk.Entry(root, textvariable=user_name_var, state='readonly')
    customer_name_entry.insert(0, user_name)
    customer_name_entry.place(x=170, y=50)

    def validate_patient_name(event):
        patient_name = patient_name_entry.get()
        if patient_name == "":
            patient_error.config(text="Fill the patient name")
        elif not all(name.isalpha() or name.isspace() for name in patient_name):
            patient_error.config(text="Username must be alphabetic")
            return
        else:
            patient_error.config(text="")
            return patient_name
    patient_error = tk.Label(root, text="", fg="red", bg="white")
    patient_error.place(x=170, y=105)

    patient_name_label = tk.Label(root, text='Patient Name:', bg="#fff")
    patient_name_label.place(x=10, y=85)
    patient_name_entry = tk.Entry(root)
    patient_name_entry.place(x=170, y=85)
    patient_name_entry.bind("<KeyRelease>", validate_patient_name)

    # Create patient name label and entry
    c.execute("select weight from users where id=?", (user_id,))
    patient_wieght = c.fetchone()[0]
    patient_wieght_label = tk.Label(root, text='Patient weight:', bg="#fff")
    patient_wieght_label.place(x=10, y=120)
    wight_var = tk.StringVar(value=patient_wieght)
    patient_wieght_entry = tk.Entry(root, textvariable=wight_var, state='readonly')
    patient_wieght_entry.insert(0, patient_wieght)
    patient_wieght_entry.place(x=170, y=120)

    c.execute("select Blood_pressure from users where id=?", (user_id,))
    patient_bp = c.fetchone()[0]
    patient_bp_label = tk.Label(root, text='Patient weight:', bg="#fff")
    patient_bp_label.place(x=10, y=155)
    bp_var = tk.StringVar(value=patient_bp)
    patient_bp_entry = tk.Entry(root, textvariable=bp_var, state='readonly')
    patient_bp_entry.insert(0, patient_bp)
    patient_bp_entry.place(x=170, y=155)

    #########################################
    # Fetch the Doctor Name with their specialization
    ######################################

    # Fetch the specializations from the database
    c.execute("SELECT DISTINCT specialization FROM doctors")
    specializations = [row[0] for row in c.fetchall()]

    # Create the specialization label and dropdown
    specialization_label = tk.Label(root, text="Select a specialization:", bg="#fff")
    specialization_label.place(x=10, y=190)

    specialization_var = tk.StringVar(root)
    specialization_var.set(specializations[0])
    specialization_dropdown = tk.OptionMenu(root, specialization_var, *specializations)
    specialization_dropdown.place(x=170, y=190)

    # Create the doctor label and dropdown
    doctor_label = tk.Label(root, text="Select a doctor:", bg="#fff")
    doctor_label.place(x=10, y=225)
    doctors_var = tk.StringVar(root)
    doctors = []
    c.execute("SELECT name FROM doctors WHERE specialization = ?", (specialization_var.get(),))
    for row in c.fetchall():
        doctors.append(row[0])
    doctors_var.set(doctors[0])
    doctor_dropdown = tk.OptionMenu(root, doctors_var, *doctors)
    doctor_dropdown.place(x=170, y=225)

    # Function to update the doctor dropdown based on the selected specialization
    def update_doctors(*args):
        doctors.clear()
        c.execute("SELECT name FROM doctors WHERE specialization = ?", (specialization_var.get(),))
        for row in c.fetchall():
            doctors.append(row[0])
        doctors_var.set(doctors[0])

        # Fetch available times for selected doctor and date
        c.execute("SELECT appointment_time FROM appointment WHERE doctor_name = ? AND appointment_date = ?",
                  (doctors_var.get(), date_entry.get()))
        booked_times = [row[0] for row in c.fetchall()]
        available_times = [time for time in times if time not in booked_times]

        times_var.set(available_times[0])  # Set the default time in the dropdown

        # Update the time dropdown menu
        menu = time_dropdown["menu"]
        menu.delete(0, "end")
        for time in available_times:
            menu.add_command(label=time, command=lambda value=time: times_var.set(value))
        date_entry.bind("<<DateEntrySelected>>", update_times)

    # Bind the update_doctors function to the specialization dropdown
    specialization_var.trace('w', update_doctors)

    def update_times(*args):
        doctor_name = doctors_var.get()
        appointment_date = date_entry.get()

        # Fetch available times for selected doctor and date
        c.execute("SELECT appointment_time FROM appointment WHERE doctor_name = ? AND appointment_date = ?",
                  (doctor_name, appointment_date))
        booked_times = [row[0] for row in c.fetchall()]
        available_times = [time for time in times if time not in booked_times]

        times_var.set(available_times[0])  # Set the default time in the dropdown

        # Update the time dropdown menu
        menu = time_dropdown["menu"]
        menu.delete(0, "end")
        for time in available_times:
            menu.add_command(label=time, command=lambda value=time: times_var.set(value))

    # create the error and success labels
    error_label = tk.Label(root, fg="red")
    error_label.place(x=400, y=200)
    success_label = tk.Label(root, fg="green")
    success_label.place(x=400, y=220)

    # Get the current date
    today = datetime.date.today()

    date_label = tk.Label(root, text="Select an appointment date:", bg="#fff")
    date_label.place(x=10, y=270)
    date_entry = DateEntry(root, width=12, background='darkblue',
                           foreground='white', borderwidth=2, year=2023, pady=10, mindate=today)
    date_entry.place(x=170, y=270)

    # create the time dropdown
    time_label = tk.Label(root, text="Select a time:", bg="#fff")
    time_label.place(x=10, y=305)
    times = ["10:00 AM","10:30 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
    times_var = tk.StringVar(root)
    times_var.set(times[0])  # Set the default time in the dropdown
    time_dropdown = tk.OptionMenu(root, times_var, *times)

    time_dropdown.place(x=170, y=305)

    # Save appointment to database
    def save_appointment(event):
        patientName = validate_patient_name(event)
        customer_name = customer_name_entry.get()
        specializations = specialization_var.get()
        doctor_name = doctors_var.get()
        appointment_time = times_var.get()
        appointment_date = date_entry.get()
        appointment_id = appointment_id_var.get().strip()
        c.execute('''Select* from appointment
                        Where doctor_name = ? AND appointment_date = ? And appointment_time = ?''',
                  (doctor_name, appointment_date, appointment_time))
        existing_appointment = c.fetchall()
        if not appointment_date:
            error_label.config(text="Enter the date")
        elif not appointment_id:
            tk.messagebox.showerror("Error", "Appointment ID is required.")
            return
        elif patientName is None:
            patient_error.config(text="Fill the patient Name")
        elif not all(name.isalpha() or name.isspace() for name in customer_name):
            tk.messagebox.showerror("Error", "Please enter a valid patient name.")
            return
        elif existing_appointment:
            tk.messagebox.showerror("Error", "This appointment slot is already booked on this Date and Time")
            return
        else:
            c.execute("INSERT INTO appointment(customer_name, patient_name, specialization, doctor_name, "
                      "appointment_id,"
                      "appointment_time, appointment_date, user_id)VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (customer_name, patientName, specializations, doctor_name, appointment_id, appointment_time, appointment_date,
                       user_id))
            conn.commit()
            tk.messagebox.showinfo("Appointment", " Appointment booked successfully!")
            window.withdraw()  # Hide the window before destroying it
            window.after(1000, window.destroy)
        # clear the entry fields and reset the dropdown menus after booking an appointment
        patient_name_entry.delete(0, 'end')
        times_var.set(times[0])
        date_entry.set_date(datetime.date.today())
        appointment_id_var.set("")

    book_appointment_button = tk.Button(root, text="Book Appointment", width=15, bg="#8A2BE2", border=0, fg="white",
                                        cursor="hand2", command=lambda event=None: save_appointment(event))
    book_appointment_button.place(x=120, y=360)
    window.mainloop()
