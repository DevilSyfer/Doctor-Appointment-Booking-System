from tkinter import *
from tkinter.ttk import *
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from fpdf import FPDF
import datetime


def view_all_appointments():
    # Create the main window
    root = Toplevel()
    root.geometry("1520x785+0+0")
    root.title("Appointment Management System")
    root.grab_set()

    # Create a frame for the search fields and search button
    search_frame = Frame(root)
    search_frame.pack(pady=10)

    def toggle_entry_fields():
        selected_option = option_var.get()
        if selected_option == 1:
            doctor_name_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)

            appointment_id_entry.config(state=tk.NORMAL)
            doctor_name_entry.config(state=tk.DISABLED)
            date_entry.config(state=tk.DISABLED)
        elif selected_option == 2:
            appointment_id_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)

            appointment_id_entry.config(state=tk.DISABLED)
            doctor_name_entry.config(state=tk.NORMAL)
            date_entry.config(state=tk.DISABLED)
        elif selected_option == 3:
            appointment_id_entry.delete(0, tk.END)
            doctor_name_entry.delete(0, tk.END)

            appointment_id_entry.config(state=tk.DISABLED)
            doctor_name_entry.config(state=tk.DISABLED)
            date_entry.config(state=tk.NORMAL)

    def search_appointment():
        # Connect to the database
        conn = sqlite3.connect('appointment.db')
        # Create a cursor
        c = conn.cursor()
        selected_option = option_var.get()
        # Get the search criteria based on the selected radio button
        if selected_option == 1:
            search_criteria = appointment_id_entry.get()
            query = "SELECT * FROM appointment WHERE appointment_id=?"
            params = (search_criteria,)
        elif selected_option == 2:
            search_criteria = doctor_name_entry.get()
            query = "SELECT * FROM appointment WHERE doctor_name=?"
            params = (search_criteria,)
        elif selected_option == 3:
            search_criteria = date_entry.get()
            query = "SELECT * FROM appointment WHERE appointment_date=?"
            params = (search_criteria,)
        else:
            messagebox.showerror("Error", "Please select a search criteria.")
            conn.close()
            return

        # Execute the query with the parameters
        c.execute(query, params)
        appointments = c.fetchall()

        # Clear the treeview
        tree.delete(*tree.get_children())

        # If appointments are found, display their details
        if appointments:
            for appointment in appointments:
                tree.insert("", 0, values=(
                    appointment[0], appointment[1], appointment[2], appointment[3], appointment[4], appointment[5]))
        # If no appointments are found, display an error message
        else:
            messagebox.showerror("Error", 'No appointments found')

        # Commit changes and close the connection
        conn.commit()
        conn.close()

    # Create a variable to store the selected search option
    option_var = tk.IntVar()
    # Create the appointment ID radio button and entry field
    appointment_id_radio = Radiobutton(search_frame, text="Appointment ID", variable=option_var, value=1,
                                       command=toggle_entry_fields)
    appointment_id_radio.pack(side=LEFT)
    appointment_id_entry = Entry(search_frame, state=DISABLED)
    appointment_id_entry.pack(side=LEFT)

    # Create the doctor name radio button and entry field
    doctor_name_radio = Radiobutton(search_frame, text="Doctor Name", variable=option_var, value=2,
                                    command=toggle_entry_fields)
    doctor_name_radio.pack(side=LEFT)
    doctor_name_entry = Entry(search_frame, state=DISABLED)
    doctor_name_entry.pack(side=LEFT)

    # Create the date radio button and calendar entry field
    today = datetime.date.today()
    date_radio = Radiobutton(search_frame, text="Date", variable=option_var, value=3, command=toggle_entry_fields)
    date_radio.pack(side=LEFT)
    date_entry = DateEntry(search_frame, state=DISABLED, mindate=today)
    date_entry.pack(side=LEFT)

    # Create a treeview to display the appointment details
    tree = Treeview(root, columns=(
        'ID', 'Patient Name', 'Doctor Name', 'Appointment Time', 'Appointment Date', 'Appointment ID'))
    tree.pack(fill=BOTH, expand=True)

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

    # Create a function to search for an appointment

    # Create a function to retrieve all appointments from the database and display them
    def display_appointments(appointment_type='booked'):
        # Connect to the database
        with sqlite3.connect('appointment.db') as conn:

            # Create a cursor
            c = conn.cursor()

        # Retrieve appointments from the database based on appointment_type
        if appointment_type == 'booked':
            c.execute("SELECT id, patient_name, doctor_name, appointment_time, "
                      "appointment_date, appointment_id FROM appointment")
        elif appointment_type == 'cancelled':
            c.execute("SELECT * FROM Canceled_Appointments")
        else:
            raise ValueError("Invalid appointment type")
        appointments = c.fetchall()

        # Clear the treeview
        tree.delete(*tree.get_children())

        # Loop through all appointments and insert them into the treeview
        for i, appointment in enumerate(appointments):
            tree.insert(parent='', index=i, iid=i, text='', values=appointment)

        # Commit changes and close the connection
        conn.commit()
        conn.close()

    def generate_pdf():
        # Retrieve all appointments from the database
        conn = sqlite3.connect('appointment.db')
        c = conn.cursor()
        c.execute(
            "SELECT patient_name, doctor_name,specialization, appointment_time, appointment_date, appointment_id  "
            "FROM appointment")
        appointments = c.fetchall()
        conn.close()

        # Generate the PDF
        pdf = FPDF()

        # Add a page to the PDF
        pdf.add_page()

        # Set font and size for the title
        pdf.set_font("Arial", size=16)

        # Add the title
        pdf.cell(0, 10, "Appointments Details", ln=True, align='C')

        # Set font and size for table content
        pdf.set_font("Arial", size=12)

        # Calculate the number of columns
        # num_columns = len(appointments[0]) if appointments else 0

        # Set column widths for the table
        col_widths = [4, 27, 27, 27, 35, 35, 30]

        # Calculate the maximum width for each column
        for appointment in appointments:
            for i, field in enumerate(appointment):
                field_width = pdf.get_string_width(str(field)) + 7
                if field_width > col_widths[i]:
                    col_widths[i] = field_width

        # Update the number of columns
        num_columns = len(col_widths)
        print(num_columns)

        # Add table headers
        headers = ['S.No', 'Patient Name', 'Doctor Name', 'Specialization', 'Appointment Time', 'Appointment Date',
                   'Appointment ID']
        for i, header in enumerate(headers):
            if i < num_columns:
                pdf.cell(col_widths[i], 10, header, border=1, ln=0, align='C')
        pdf.ln()

        # Add appointments to the table
        serial_no = 1  # Initialize the serial number
        for appointment in appointments:
            pdf.cell(col_widths[0], 10, str(serial_no), border=1, ln=0, align='C')  # Add the serial number
            serial_no += 1  # Increment the serial number
            for i, field in enumerate(appointment):
                if i < num_columns:
                    pdf.cell(col_widths[i + 1], 10, str(field), border=1, ln=0, align='C')  # Adjust column index
            pdf.ln()

        # Save the PDF
        pdf.output("appointments.pdf")
        messagebox.showinfo("Success", "PDF generated successfully.")

    # Create a button to display all appointments
    display_button = Button(root, text="Booked Appointments",
                            command=lambda: display_appointments(appointment_type='booked'))
    display_button.pack()

    cancel_button = Button(root, text="Cancelled Appointments",
                           command=lambda: display_appointments(appointment_type='cancelled'))
    cancel_button.pack()

    # Create a button to search for an appointment
    search_button = Button(search_frame, text="Search", command=search_appointment)
    search_button.pack(side=LEFT, padx=10)

    generate_pdf_button = Button(search_frame, text="Generate PDF", command=generate_pdf)
    generate_pdf_button.pack(side=LEFT)

    # Start the main loop
    root.mainloop()

# view_all_appointments()
