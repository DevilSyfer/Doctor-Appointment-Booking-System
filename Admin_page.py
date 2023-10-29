from logout import show_introduction
import tkinter as tk
import sqlite3
from view_appointment import view_all_appointments
from add_doctor import Add_Doctors
from View_Doctors import doctor_list
from Delete_doctor import delete_doctor
from Notification import show_appointments
from upadate_appoin import update_appointment
from admin_cancel_appointment import Cancel_appointments

with sqlite3.connect('appointment.db') as conn:
    cursor = conn.cursor()


def Admin_Landing_page():
    window = tk.Tk()
    window.title("Doctor Appointment System")
    window.geometry("1520x785+0+0")
    window.configure(bg="#fff")
    window.grab_set()
    window.resizable(False, False)

    def log_out():
        window.destroy()
        show_introduction()

    def open_menu():
        menu = tk.Menu(window, tearoff=False)
        menu.add_command(label='View Doctor', command=doctor_list)
        menu.add_command(label='Add Doctors', command=Add_Doctors)
        menu.add_command(label='Delete Doctors', command=delete_doctor)
        try:
            menu.tk_popup(window.winfo_pointerx(), window.winfo_pointery(), 0)
        finally:
            menu.grab_release()

    def open_menu2():
        menu = tk.Menu(window, tearoff=False)
        menu.add_command(label='Update Appointment', command=update_appointment)
        menu.add_command(label='Cancel Appointment', command=Cancel_appointments)
        try:
            menu.tk_popup(window.winfo_pointerx(), window.winfo_pointery(), 0)
        finally:
            menu.grab_release()

    img1 = tk.PhotoImage(file=r"D:\Pycharm\project testing\images\stethoscope.png")
    tk.Label(window, image=img1, bg="white").place(x=100, y=60)
    img = tk.PhotoImage(file=r"D:\Pycharm\project testing\images\login3.png")
    tk.Label(window, image=img, bg="white").place(x=100, y=170)

    frame2 = tk.Frame(window, width=650, height=500, bg="white")
    frame2.place(x=750, y=100)

    button1 = tk.Button(frame2, text="Doctors", fg="black", bg="white", cursor="hand2", border=0,
                        font=("Microsoft YaHei UI Light", 11), command=open_menu)
    button1.place(x=0, y=0)

    button2 = tk.Button(frame2, text="View Appointment", fg="black", cursor="hand2", border=0, bg="white",
                        font=("Microsoft YaHei UI Light", 11), command=view_all_appointments)
    button2.place(x=90, y=0)

    button3 = tk.Button(frame2, text="Changing Appointment", fg="black", cursor="hand2", border=0, bg="white",
                        font=("Microsoft YaHei UI Light", 11), command=open_menu2)
    button3.place(x=270, y=0)

    button4 = tk.Button(frame2, text="Request", fg="black", cursor="hand2", border=0, bg="white",
                        font=("Microsoft YaHei UI Light", 11),
                        command=lambda: [notification_badge.config(text=""), show_appointments()])
    button4.place(x=450, y=0)
    # Query the database for the number of appointment requests
    cursor.execute("SELECT COUNT(*) FROM appointment_request")
    num_requests = cursor.fetchone()[0]

    # Create the notification badge
    notification_badge = tk.Label(frame2, text=num_requests, fg="red", bg="white")
    notification_badge.place(x=525, y=0)

    # Add the notification badge to the request button
    button4.config(compound="left", padx=5, border=0)
    button4.place(x=460, y=0)

    # Logout button and label
    button5 = tk.Button(frame2, text="Log out", fg="black", cursor="hand2", border=0, bg="white",
                        font=("Microsoft YaHei UI Light", 11), command=log_out)
    button5.place(x=550, y=0)

    label1 = tk.Label(frame2, text="Find Your Perfect Doctor", fg="#2F326E", bg="white",
                      font=("Neue Metana Bold", 32, "bold"))
    label1.place(x=0, y=140)
    text = tk.Label(frame2,
                text='''Healthcare is an essential part of our lives. It encompasses 
everything from preventative care to emergency treatment,
and it affects people of all ages, genders, and backgrounds. 
Good healthcare is important not only for our physical health 
but also for our mental and emotional well-being. That's why
it's crucial have access to high-quality healthcare services 
that are affordable and accessible to everyone.''',
                    fg="black", bg="white", font=("Microsoft YaHei UI Light", 12), justify='left', anchor='w')
    text.place(x=0, y=230)

    window.mainloop()
