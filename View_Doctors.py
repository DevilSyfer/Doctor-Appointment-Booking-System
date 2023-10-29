import tkinter as tk
import sqlite3
from tkinter import ttk


def doctor_list():
    # create database connection and cursor
    with sqlite3.connect('appointment.db') as conn:
        c = conn.cursor()
    # create the tkinter window and widgets

    # create the doctors table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY,
                name TEXT,
                specialization TEXT
                )''')

    # function to retrieve all doctors from the database
    def get_doctors():
        # execute a SELECT statement to get all doctors
        c.execute("SELECT id, name, specialization FROM doctors order by specialization")
        # fetch all the rows returned by the SELECT statement
        rows = c.fetchall()
        print(rows)
        # return the rows
        return rows

    # create the tkinter window and widgets
    root = tk.Tk()
    root.geometry("1520x785+0+0")
    root.title('Doctors')

    # create a treeview widget to display the doctors
    tree = ttk.Treeview(root)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # add columns to the treeview
    tree['columns'] = ('Doctor ID', 'Name', 'Specialization')

    # format the columns
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('Doctor ID', width=150, anchor=tk.W)
    tree.column('Name', width=150, anchor=tk.W)
    tree.column('Specialization', width=150, anchor=tk.W)

    # add headings to the columns
    tree.heading('#0', text='', anchor=tk.W)
    tree.heading('Doctor ID', text='Doctor ID', anchor=tk.W)
    tree.heading('Name', text='Name', anchor=tk.W)
    tree.heading('Specialization', text='Specialization', anchor=tk.W)

    # retrieve the doctors from the database
    doctors = get_doctors()

    # iterate over the doctors and insert them into the treeview
    for i, doctor in enumerate(doctors):
        tree.insert(parent='', index=i, iid=i, text='', values=doctor)

    # start the main loop
    root.mainloop()

    # close the database connection
    conn.close()
# doctor_list()