import tkinter as tk
import sqlite3
from tkinter import ttk


def show_appointments():
    # Connect to the database
    with sqlite3.connect('appointment.db') as conn:
        cursor = conn.cursor()

    # Open a new window for displaying the appointments
    window = tk.Toplevel()
    window.title("Appointment Details")
    window.geometry("1520x785+0+0")
    window.grab_set()

    # Create a treeview widget for displaying the appointments
    tree = ttk.Treeview(window)
    tree["columns"] = ('ID', 'Patient Name', 'Doctor Name', 'Appointment Time', 'Appointment Date', 'Appointment ID')

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

    # Query the database for the appointment details
    cursor.execute("SELECT * FROM appointment_request")
    rows = cursor.fetchall()

    # Loop through all appointments and insert them into the treeview
    for i, appointment in enumerate(rows):
        tree.insert(parent='', index=i, iid=i, text='', values=appointment)

    tree.pack(expand=True, fill=tk.BOTH)
    # Run the program
    window.mainloop()
