import tkinter as tk
import sqlite3
from book_appointment2 import Book_Appointment
from User_View_Appointments import user_appointment
from Cancel_appointment_by_admin import cancel_user_appointment
from Cancel_Appointment import cancel_appointment
from Request_page import change_appointment
from logout import show_introduction


def User_Landing_page(user_id):
    window = tk.Tk()
    window.title("Doctor Appointment System")
    window.geometry("1520x785+0+0")
    window.configure(bg="#fff")
    window.resizable(False, False)

    def Log_out():
        window.destroy()
        show_introduction()

    def open_menu2():
        menu = tk.Menu(window, tearoff=False)
        menu.add_command(label='Booked Appointment', command=lambda: user_appointment(user_id))
        menu.add_command(label='Cancelled Appointment', command=lambda: cancel_user_appointment(user_id))
        try:
            menu.tk_popup(window.winfo_pointerx(), window.winfo_pointery(), 0)
        finally:
            menu.grab_release()

    img1 = tk.PhotoImage(file=r"D:\Pycharm\project testing\images\stethoscope.png")
    tk.Label(window, image=img1, bg="white").place(x=100, y=60)
    img = tk.PhotoImage(file=r"D:\Pycharm\project testing\images\landing.png")
    tk.Label(window, image=img, bg="white").place(x=100, y=170)

    frame2 = tk.Frame(window, width=650, height=550, bg="WHITE")
    frame2.place(x=750, y=100)

    # create the main dropdown menu for specializations
    main_menu = tk.Menubutton(frame2, text="Doctors", border=0, bg='white', font=("Microsoft YaHei UI Light", 11))
    main_menu.menu = tk.Menu(main_menu, tearoff=0)
    main_menu["menu"] = main_menu.menu

    # connect to the database and fetch data for the main menu
    with sqlite3.connect('appointment.db') as conn:
        c = conn.cursor()
    c.execute("SELECT DISTINCT specialization FROM doctors")
    data = c.fetchall()

    # create a new submenu for each specialization
    for item in data:
        submenu = tk.Menu(main_menu.menu, tearoff=0)
        c.execute("SELECT name FROM doctors WHERE specialization=?", (item[0],))
        sub_data = c.fetchall()
        for sub_item in sub_data:
            submenu.add_command(label=sub_item[0])
        main_menu.menu.add_cascade(label=item[0], menu=submenu)

    # add the main menu to the window
    main_menu.place(x=0, y=0)

    button2 = tk.Button(frame2, text="Scheduled Appointment", fg="black", cursor="hand2", border=0, bg="white",
                        font=("Microsoft YaHei UI Light", 11), command=open_menu2)
    button2.place(x=90, y=0)

    button3 = tk.Button(frame2, text="Cancel Appointment", fg="black", cursor="hand2", border=0, bg="white",
                        font=("Microsoft YaHei UI Light", 11), command=lambda: cancel_appointment(window, user_id))
    button3.place(x=285, y=0)
    button4 = tk.Button(frame2, text="Request", fg="black", cursor="hand2", border=0, bg="white",
                        font=("Microsoft YaHei UI Light", 11), command=lambda: change_appointment(window, user_id))
    button4.place(x=460, y=0)

    button5 = tk.Button(frame2, text="Log out", fg="black", cursor="hand2", border=0, bg="white",
                        font=("Microsoft YaHei UI Light", 11), command=Log_out)
    button5.place(x=550, y=0)

    label1 = tk.Label(frame2, text="Find Your Perfect Doctor", fg="#2F326E", bg="white",
                      font=("Neu Meta Bold", 32, "bold"))
    label1.place(x=0, y=190)
    text = tk.Label(frame2, text='''Healthcare is an essential part of our lives. It encompasses
everything from preventative care to emergency treatment,
and it affects people of all ages, genders, and backgrounds.
Good healthcare is important not only for our physical health
but also for our mental and emotional well-being. That's why
it's crucial have access to high-quality healthcare services
that are affordable and accessible to everyone.''',
                    fg="black", bg="white", font=("Microsoft YaHei UI Light", 12), justify='left', anchor='nw')
    text.place(x=0, y=300)

    button4 = tk.Button(frame2, text="Schedule Your Visit", fg="white", cursor="hand2", bg="#5158D3", border=0,
                        font=("Eras Medium ITC", 11), command=lambda: Book_Appointment(window, user_id))
    button4.place(x=0, y=510)

    window.mainloop()
