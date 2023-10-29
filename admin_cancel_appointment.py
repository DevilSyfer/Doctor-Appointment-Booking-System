import tkinter as tk
from tkinter import *
import sqlite3
from tkinter import ttk
from PIL import Image, ImageTk


with sqlite3.connect('appointment.db') as conn:
    c = conn.cursor()


def Cancel_appointments():
    root = tk.Toplevel()
    root.geometry("1520x785+0+0")
    root.title("Cancel Appointments")
    root.grab_set()

    # Create a main frame to hold the two frames
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create a frame to hold the button and the cancel button
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=10)

    # Create a frame to hold the appointment details
    details_frame = tk.Frame(main_frame)
    details_frame.pack(fill=tk.BOTH, expand=True)

    # Create a label for displaying the appointment details
    appointment_label = tk.Label(details_frame, text="")
    appointment_label.pack()

    # Create a function to cancel the appointment using the appointment ID
    def cancel_appointment():
        # Create a popup window for user input
        popup = tk.Toplevel(root)
        popup.title("Cancel Appointment")
        popup.geometry("925x600+300+150")
        popup.resizable(False, False)
        popup.configure(bg="#fff")

        heading = tk.Label(popup,
                           text='''Cancel Appointment''', bg='#fff', fg="#483D8B",
                           font=("Bell MT", 28, "bold"), justify='left')
        heading.place(x=500, y=50)

        # Open and resize the image using PIL (Pillow)
        img = Image.open(r"D:\Pycharm\project testing\images\cancel.png")
        resized_img = img.resize((500, 500), Image.ANTIALIAS)

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
            appointment_label = tk.Label(popup, text='Appointment ID:', bg='#fff')
            appointment_label.place(x=590, y=150)

            appointment_dropdown = tk.OptionMenu(popup, appointment_var, *appointments)
            appointment_dropdown.place(x=600, y=180)

            # Create a frame to hold the appointment details
            details_frame = tk.Frame(popup, bg='#fff')
            details_frame.place(x=520, y=220)

            # Create the labels and entry fields with default values
        patient_name_label = tk.Label(details_frame, text="Patient Name:", bg='#fff')
        patient_name_label.pack(side=tk.TOP)
        patient_Name_var = tk.StringVar(value="")
        patient_name_entry = tk.Entry(details_frame, textvariable=patient_Name_var, state="readonly")
        patient_name_entry.pack(side=tk.TOP)

        doctor_label = tk.Label(details_frame, text="Doctor Name:", bg='#fff')
        doctor_label.pack(side=tk.TOP)
        doctor_Name_var = tk.StringVar(value="")
        doctor_entry = tk.Entry(details_frame, textvariable=doctor_Name_var, state="readonly")
        doctor_entry.pack(side=tk.TOP)

        date_label = tk.Label(details_frame, text="Selected an appointment time:", bg='#fff')
        date_label.pack(side=tk.TOP)
        date_var = tk.StringVar(value="")
        date_entry = tk.Entry(details_frame, textvariable=date_var, state="readonly")
        date_entry.pack(side=tk.TOP)

        time_label = tk.Label(details_frame, text="Selected a appointment date:", bg='#fff')
        time_label.pack(side=tk.TOP)
        time_var = tk.StringVar(value="")
        time_entry = tk.Entry(details_frame, textvariable=time_var, state="readonly")
        time_entry.pack(side=tk.TOP)

        reason_label = tk.Label(details_frame, text="Enter reason for cancellation:", bg='#fff')
        reason_label.pack(side=tk.TOP)
        reason_textbox = tk.Text(details_frame, height=5, width=30, borderwidth=1, relief="solid")
        reason_textbox.pack(side=tk.TOP)

        def update_appointment_details(*args):
            # Get the appointment ID from the search box
            appointment_id = appointment_var.get()

            # Search for the appointment with the given ID
            c.execute("SELECT * FROM appointment WHERE appointment_id=?", (appointment_id,))
            appointment = c.fetchone()

            if appointment:
                # Update the values of the entry fields with the data from the selected appointment
                patient_Name_var.set(appointment[1])
                doctor_Name_var.set(appointment[2])
                date_var.set(appointment[3])
                time_var.set(appointment[4])

        # Bind the update_appointment_details function to the dropdown menu
        appointment_var.trace('w', update_appointment_details)

        # Create a function to delete the appointment and close the popup window
        def delete_appointment():
            # Get the appointment ID entered by the user
            appointment_id = appointment_var.get()
            c.execute("SELECT * FROM appointment WHERE appointment_id=?", (appointment_id,))
            appoint = c.fetchone()
            # Create appointments table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS Canceled_Appointments
                                               (id INTEGER,
                                                customer_name TEXT,
                                                patient_name TEXT,
                                                doctor_name TEXT,
                                                specialization TEXT,
                                                appointment_time TEXT,
                                                appointment_date TEXT,
                                                appointment_id TEXT,
                                                user_id TEXT,
                                                cancel_reason TEXT)''')
            cancel_reason = reason_textbox.get("1.0", END).strip()
            if appointment_id:
                # Insert the appointment details into the Canceled Appointments table
                c.execute('''INSERT INTO Canceled_Appointments (id,customer_name, patient_name, doctor_name, 
                specialization, appointment_time, appointment_date, appointment_id, user_id,cancel_reason ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (
                              appoint[0], appoint[1], appoint[2], appoint[3], appoint[4], appoint[5],
                              appoint[6], appoint[7], appoint[8], cancel_reason))
            c.execute("Delete from appointment where appointment_id=?", (appointment_id,))
            c.execute("Delete from appointment_request where appointment_id=?", (appointment_id,))
            # Commit changes and close the connection
            conn.commit()
            conn.close()
            # Refresh the treeview
            display_appointments()

            # Close the popup window
            popup.destroy()

        # Create a button to delete the appointment
        delete_button = tk.Button(popup, text="Cancel", command=delete_appointment)
        delete_button.place(x=570, y=500)

        # Create a button to cancel the operation and close the popup window
        cancel_button = tk.Button(popup, text="Back", command=popup.destroy)
        cancel_button.place(x=670, y=500)

    # Create a function to retrieve all appointments from the database and display them
    def display_appointments():
        # Clear the label
        appointment_label.config(text="")

        # Clear the treeview
        for child in tree.get_children():
            tree.delete(child)

        # Retrieve all appointments from the database for the logged in user
        with sqlite3.connect('appointment.db') as conn:
            c = conn.cursor()
        c.execute("SELECT id, patient_name, doctor_name, appointment_time, "
                  "appointment_date, appointment_id FROM appointment")
        appointments = c.fetchall()

        # Loop through all appointments and insert them into the treeview
        for i, appointment in enumerate(appointments):
            tree.insert(parent='', index=i, iid=i, text='', values=appointment)

        # Commit changes and close the connection
        conn.commit()
        conn.close()

    # Create the treeview widget
    tree = ttk.Treeview(details_frame)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Define the columns
    tree['columns'] = (
        'ID', 'Patient Name', 'Doctor Name', 'Appointment Time', 'Appointment Date', 'Appointment ID')

    # Format the columns
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID', width=100, anchor=tk.W)
    tree.column('Patient Name', width=150, anchor=tk.W)
    tree.column('Doctor Name', width=150, anchor=tk.W)
    tree.column('Appointment Time', width=150, anchor=tk.W)
    tree.column('Appointment Date', width=150, anchor=tk.W)
    tree.column('Appointment ID', width=100, anchor=tk.W)

    # Add headings to the columns
    tree.heading('#0', text='', anchor=tk.W)
    tree.heading('ID', text='ID', anchor=tk.W)
    tree.heading('Patient Name', text='Patient Name', anchor=tk.W)
    tree.heading('Doctor Name', text='Doctor Name', anchor=tk.W)
    tree.heading('Appointment Time', text='Appointment Time', anchor=tk.W)
    tree.heading('Appointment Date', text='Appointment Date', anchor=tk.W)
    tree.heading('Appointment ID', text='Appointment ID', anchor=tk.W)

    # Create a button to display all appointments
    display_button = tk.Button(button_frame, text="Display All Appointments", command=display_appointments)
    display_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Create a button to cancel an appointment
    cancel_button = tk.Button(button_frame, text="Cancel Appointment", command=cancel_appointment)
    cancel_button.pack(side=tk.LEFT, padx=10, pady=10)
    root.mainloop()
# Cancel_appointments()