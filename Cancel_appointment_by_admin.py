import tkinter as tk
import sqlite3
from tkinter import ttk


def cancel_user_appointment(user_id):
    root = tk.Toplevel()
    root.geometry("1520x785+0+0")
    root.title("Cancel Appointment")
    root.grab_set()
    # Create a main frame to hold the two frames
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Create a frame to hold the button
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=20)

    # Create a frame to hold the appointment details
    details_frame = tk.Frame(main_frame)
    details_frame.pack(fill=tk.BOTH, expand=True)

    # Create a label for displaying the appointment details
    appointment_label = tk.Label(details_frame, text="")
    appointment_label.pack()

    # Create a function to retrieve all appointments from the database and display them
    def display_appointments():
        # Clear the label
        appointment_label.config(text="")

        # Clear the treeview
        for child in tree.get_children():
            tree.delete(child)

        # Retrieve all appointments from the database for the logged-in user
        with sqlite3.connect('appointment.db') as conn:
            c = conn.cursor()
        c.execute(
            "SELECT ID, patient_name, doctor_name, appointment_time, appointment_date, appointment_id, "
            "specialization, cancel_reason FROM Canceled_Appointments WHERE user_id=?",
            (user_id,))
        appointments = c.fetchall()

        # Loop through all appointments and insert them into the treeview
        for i, appointment in enumerate(appointments):
            values = list(appointment)
            values.pop(-2)  # Remove the user_id column
            tree.insert(parent='', index=i, iid=i, text='', values=values)

        # Commit changes and close the connection
        conn.commit()
        conn.close()

    # Create the treeview widget
    tree = ttk.Treeview(details_frame)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Define the columns
    tree['columns'] = (
        'ID', 'Patient Name', 'Doctor Name', 'Appointment Time', 'Appointment Date', 'Appointment ID', 'Cancel Reason')

    # Format the columns
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('ID', width=100, anchor=tk.W)
    tree.column('Patient Name', width=150, anchor=tk.W)
    tree.column('Doctor Name', width=150, anchor=tk.W)
    tree.column('Appointment Time', width=150, anchor=tk.W)
    tree.column('Appointment Date', width=150, anchor=tk.W)
    tree.column('Appointment ID', width=100, anchor=tk.W)
    tree.column('Cancel Reason', width=150, anchor=tk.W)

    # Add headings to the columns
    tree.heading('#0', text='', anchor=tk.W)
    tree.heading('ID', text='ID', anchor=tk.W)
    tree.heading('Patient Name', text='Patient Name', anchor=tk.W)
    tree.heading('Doctor Name', text='Doctor Name', anchor=tk.W)
    tree.heading('Appointment Time', text='Appointment Time', anchor=tk.W)
    tree.heading('Appointment Date', text='Appointment Date', anchor=tk.W)
    tree.heading('Appointment ID', text='Appointment ID', anchor=tk.W)
    tree.heading('Cancel Reason', text='Cancel Reason', anchor=tk.W)

    # Create a button to display all appointments
    display_button = tk.Button(root, text="Display All Cancelled Appointments", command=display_appointments)
    display_button.place(x=650, y=20)

    # Start the main loop
    root.mainloop()
