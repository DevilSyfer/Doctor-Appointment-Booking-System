from tkinter import *
from tkinter.ttk import *
import sqlite3
import tkinter as tk
from tkcalendar import DateEntry
import datetime
from PIL import ImageTk, Image


def update_appointment():
    # Create the main window
    root = Toplevel()
    root.geometry("1520x785+0+0")
    root.title("Appointment Management System")
    root.grab_set()
    root.configure(bg="red")
    # Create a main frame to hold the two frames
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create a frame to hold the button and the cancel button
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=10)

    # Create a frame to hold the appointment details
    popup = tk.Frame(main_frame)
    popup.pack(fill=tk.BOTH, expand=True)

    # Create a treeview to display the appointment details
    tree = Treeview(popup, columns=('ID', 'Patient Name', 'Doctor Name', "Specialization",
                                    'Appointment Time', 'Appointment Date',
                                    'Appointment ID'))
    tree.pack(side=LEFT, fill=BOTH, expand=1)

    # Format the columns
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID', width=100, anchor=tk.W)
    tree.column('Patient Name', width=150, anchor=tk.W)
    tree.column('Doctor Name', width=150, anchor=tk.W)
    tree.column('Specialization', width=150, anchor=tk.W)
    tree.column('Appointment Time', width=150, anchor=tk.W)
    tree.column('Appointment Date', width=150, anchor=tk.W)
    tree.column('Appointment ID', width=100, anchor=tk.W)

    # Add headings to the columns
    tree.heading('#0', text='', anchor=tk.W)
    tree.heading('ID', text='ID', anchor=tk.W)
    tree.heading('Patient Name', text='Patient Name', anchor=tk.W)
    tree.heading('Doctor Name', text='Doctor Name', anchor=tk.W)
    tree.heading('Specialization', text='Specialization', anchor=tk.W)
    tree.heading('Appointment Time', text='Appointment Time', anchor=tk.W)
    tree.heading('Appointment Date', text='Appointment Date', anchor=tk.W)
    tree.heading('Appointment ID', text='Appointment ID', anchor=tk.W)

    # Create a function to search for an appointment by its ID
    def search_appointment():
        # Create a popup window for user input
        popup = tk.Toplevel(root)
        popup.title("Update Appointment")
        popup.geometry("925x600+300+150")
        popup.configure(bg="#fff")
        popup.grab_set()
        popup.resizable(False, False)
        heading = tk.Label(popup,
                           text='''Update Appointment''', bg='#fff', fg="#483D8B",
                           font=("Bell MT", 28, "bold"), justify='left')
        heading.place(x=500, y=70)

        # Open and resize the image using PIL (Pillow)
        img = Image.open(r"D:\Pycharm\project testing\images\update.png")
        resized_img = img.resize((500, 550), Image.ANTIALIAS)

        # Convert the resized image to a PhotoImage object
        photoimg = ImageTk.PhotoImage(resized_img)

        # Create a label for the image
        label1 = tk.Label(popup, image=photoimg, border=0)
        label1.place(x=0, y=50)
        label1.image = photoimg

        with sqlite3.connect('appointment.db') as conn:
            c = conn.cursor()
            # Get all appointment IDs from the database
            c.execute("SELECT appointment_id FROM appointment")
            appointments = [row[0] for row in c.fetchall()]

            # Create Appointment ID label and dropdown menu
            appointment_var = tk.StringVar(popup)
            if appointments:
                appointment_var.set(appointments[0])
            else:
                appointment_var.set('')
            appointment_label = tk.Label(popup, text='Appointment ID:', bg="#fff")
            appointment_label.place(x=500, y=200)

            appointment_dropdown = tk.OptionMenu(popup, appointment_var, *appointments)
            appointment_dropdown.place(x=660, y=200)

            # Create the labels and entry fields with default values
        patient_name_label = tk.Label(popup, text="Patient Name:", bg="#fff")
        patient_name_label.place(x=500, y=250)
        patient_Name_var = tk.StringVar(value="")
        patient_name_entry = tk.Entry(popup, textvariable=patient_Name_var, state="readonly")
        patient_name_entry.place(x=660, y=250)

        #########################################
        # Fetch the Doctor Name with their specialization
        ########################################

        # Fetch the specializations from the database
        c.execute("SELECT DISTINCT specialization FROM doctors")
        specializations = [row[0] for row in c.fetchall()]

        # Create the specialization label and dropdown
        specialization_label = tk.Label(popup, text="Select specialization:", bg="#fff")
        specialization_label.place(x=500, y=300)

        specialization_var = tk.StringVar(popup)
        specialization_var.set(specializations[0])
        specialization_dropdown = tk.OptionMenu(popup, specialization_var, *specializations)
        specialization_dropdown.place(x=660, y=300)

        doctor_label = tk.Label(popup, text="Doctor Name:", bg="#fff")
        doctor_label.place(x=500, y=350)
        doctors_var = tk.StringVar(root)
        doctors = []
        c.execute("SELECT name FROM doctors WHERE specialization = ?", (specialization_var.get(),))
        for row in c.fetchall():
            doctors.append(row[0])
        doctors_var.set(doctors[0])
        doctor_dropdown = tk.OptionMenu(popup, doctors_var, *doctors)
        doctor_dropdown.place(x=660, y=350)

        # Function to update the doctor dropdown based on the selected specialization
        def update_doctors(*args):
            doctors.clear()
            c.execute("SELECT name FROM doctors WHERE specialization = ?", (specialization_var.get(),))
            for row in c.fetchall():
                doctors.append(row[0])
            doctors_var.set(doctors[0])
            menu = doctor_dropdown["menu"]
            menu.delete(0, "end")
            for doctor in doctors:
                menu.add_command(label=doctor, command=(doctors_var, doctor))

        # Bind the update_doctors function to the specialization dropdown
        specialization_var.trace('w', update_doctors)

        time_label = tk.Label(popup, text="Selected appointment time:", bg="#fff")
        time_label.place(x=500, y=400)
        times = ["10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]
        time_var = tk.StringVar(popup)
        time_var.set(times[0])
        time_dropdown = tk.OptionMenu(popup, time_var, *times)
        time_dropdown.place(x=660, y=400)

        today = datetime.date.today()
        date_label = tk.Label(popup, text="Selected a appointment date:", bg="#fff")
        date_label.place(x=500, y=450)
        date_entry = DateEntry(popup, width=12, background='darkblue',
                               foreground='white', borderwidth=2, year=2023, pady=10, mindate=today)
        date_entry.place(x=660, y=450)

        def update_appointment_details(*args):
            appointment_id = appointment_var.get()

            # Search for the appointment with the given ID
            c.execute("SELECT * FROM appointment WHERE appointment_id=?", (appointment_id,))
            appointment = c.fetchone()

            if appointment:
                # Update the values of the entry fields with the data from the selected appointment
                patient_Name_var.set(appointment[1])

        # Bind the update_appointment_details function to the dropdown menu
        appointment_var.trace('w', update_appointment_details)

        # Create a function to update the appointment details
        def save_changes():
            # Get the updated details from the entry boxes
            appointment_id = appointment_var.get()
            patient_name = patient_name_entry.get()
            doctor_name = doctors_var.get()
            date = date_entry.get()
            time = time_var.get()

            # Update the appointment with the new details
            c.execute("UPDATE appointment SET patient_name=?, doctor_name=?, appointment_date=?, "
                      "appointment_time=? WHERE appointment_id=?",
                      (patient_name, doctor_name, date, time, appointment_id))
            c.execute("Delete from appointment_request where appointment_id=?", (appointment_id,))
            # Display a success message
            success_label = Label(popup, text="Appointment updated successfully!")
            success_label.pack()

            # Commit changes and close the connection
            conn.commit()
            conn.close()

            # Destroy the update window and show the search button
            popup.destroy()
            search_button.pack()

        # Create a button to save the changes
        save_button = Button(popup, text="Save Changes", command=save_changes)
        save_button.place(x=600, y=500)

    # Create a function to retrieve all appointments from the database and display them
    def display_appointments():
        # Connect to the database
        with sqlite3.connect('appointment.db') as conn:
            # Create a cursor
            c = conn.cursor()
            # Clear the label

        # Retrieve all appointments from the database
        c.execute("SELECT id,patient_name, doctor_name,specialization, appointment_time,"
                  " appointment_date, appointment_id FROM appointment")
        appointments = c.fetchall()

        # Clear the treeview
        tree.delete(*tree.get_children())

        # Loop through all appointments and insert them into the treeview
        for i, appointment in enumerate(appointments):
            tree.insert(parent='', index=i, iid=i, text='', values=appointment)

        # Commit changes and close the connection
        conn.commit()
        conn.close()

    # Create a button to display all appointments
    display_button = Button(button_frame, text="Display All Appointments", command=display_appointments)
    display_button.pack(side=LEFT, padx=10, pady=10)

    # Create a button to search for an appointment
    search_button = Button(button_frame, text="Update Appointment", command=search_appointment)
    search_button.pack(side=LEFT, padx=10)
    # Start the main loop
    root.mainloop()


