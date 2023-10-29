import tkinter as tk
import sqlite3
from tkinter import ttk
from PIL import ImageTk
from PIL import Image

with sqlite3.connect('appointment.db') as conn:
    c = conn.cursor()


def cancel_appointment(window, user_id):
    root = tk.Toplevel()
    root.geometry("1520x785+0+0")
    root.title("Booked Appointments")

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

    # Create a function to cancel the appointment using the appointment ID
    def cancel_appointments():
        # Create a popup window for user input
        popup = tk.Toplevel(root)
        popup.title("Cancel Appointment")
        popup.geometry("700x400+400+200")
        popup.configure(bg="#fff")
        popup.grab_set()

        heading = tk.Label(popup,
                           text='''Cancel
Appointment''', bg='#fff', fg="#483D8B",
                           font=("Bell MT", 28, "bold"), justify='left')
        heading.place(x=400, y=70)
        # Open and resize the image using PIL (Pillow)
        img = Image.open(r"D:\Pycharm\project testing\images\cancel.png")
        resized_img = img.resize((400, 400), Image.ANTIALIAS)

        # Convert the resized image to a PhotoImage object
        photoimg = ImageTk.PhotoImage(resized_img)

        # Create a label for the image
        label1 = tk.Label(popup, image=photoimg, border=0)
        label1.place(x=0, y=0)
        label1.image = photoimg
        with sqlite3.connect('appointment.db') as conn:
            c = conn.cursor()
        # Get all appointment IDs from the database
        c.execute("SELECT appointment_id FROM appointment where appointment_id=?", (user_id,))
        appointments = [row[0] for row in c.fetchall()]

        # Create Appointment ID label and dropdown menu
        appointment_var = tk.StringVar(popup)
        if appointments:
            appointment_var.set(appointments[0])
        else:
            appointment_var.set('')
        appointment_label = tk.Label(popup, text='Appointment ID:')
        appointment_label.place(x=400, y=200)

        appointment_dropdown = tk.OptionMenu(popup, appointment_var, *(appointments if appointments else ['']))
        appointment_dropdown.place(x=500, y=200)

        # Create a function to delete the appointment and close the popup window
        def delete_appointment():
            # Get the appointment ID entered by the user
            appointment_id = appointment_var.get()

            # Delete the appointment from the database
            c.execute("DELETE FROM appointment WHERE appointment_id=?", (appointment_id,))
            conn.commit()
            conn.close()

            # Refresh the treeview
            display_appointments()

            # Close the popup window
            popup.destroy()

        # Create a button to delete the appointment
        delete_button = tk.Button(popup, text="Cancel", command=delete_appointment)
        delete_button.place(x=600, y=200)

        # Create a button to cancel the operation and close the popup window
        cancel_button = tk.Button(popup, text="Back", command=popup.destroy)
        cancel_button.place(x=600, y=250)

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
        c.execute("SELECT id, patient_name, doctor_name, appointment_time, appointment_date, appointment_id FROM "
                  "appointment WHERE user_id=?", (user_id,))
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
    display_button = tk.Button(root, text="Display All Appointments", command=display_appointments)
    display_button.place(x=600, y=20)

    # Create a button to cancel an appointment
    cancel_button = tk.Button(root, text="Cancel Appointment", command=cancel_appointments)
    cancel_button.place(x=750, y=20)
    root.mainloop()
