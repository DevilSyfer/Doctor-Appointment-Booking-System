import tkinter as tk
from tkinter import messagebox
from landing_page import User_Landing_page
from Admin_page import Admin_Landing_page
import sqlite3
import re
from logout import show_introduction


def Login():
    # connect to the database
    with sqlite3.connect('appointment.db') as conn:
        # create the cursor
        cursor = conn.cursor()

    # Create a table for the user
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, '
                   'username TEXT UNIQUE, password TEXT,weight text, Blood_pressure text )')

    window = tk.Tk()
    window.title("Signin")
    window.geometry("1520x785+0+0")
    window.configure(bg="#fff")
    window.resizable(False, False)

    def Log_out():
        window.destroy()
        show_introduction()

    def signin():
        username = user.get()
        password = code.get()
        cursor.execute("Select  * from users where username=? AND password=?", (username, password))
        users = cursor.fetchone()
        if users:
            messagebox.showinfo("Login", "Login Successful")
            cursor.execute("select id from users where username=? and password=?", (username, password))
            user_id = cursor.fetchone()[0]
            window.destroy()
            User_Landing_page(user_id)
        elif username == 'admin' and password == "12":
            window.destroy()
            Admin_Landing_page()
        else:
            messagebox.showerror('Login', 'Login Failed')

    img = tk.PhotoImage(file=r"D:\Pycharm\project testing\images\login.png")
    tk.Label(window, image=img, bg="white").place(x=300, y=250)

    frame = tk.Frame(window, width=350, height=350, bg="white")
    frame.place(x=800, y=260)

    heading = tk.Label(frame, text="Sign in", fg="#57a1f8", bg="white", font=("Microsoft YaHei UI Light", 23, "bold"))
    heading.place(x=120, y=5)

    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(b):
        name = user.get()
        if name == "":
            user.insert(0, "Username")
            user.config(show='')

    user = tk.Entry(frame, width=20, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
    user.place(x=30, y=80)
    user.insert(0, "Username")
    user.bind('<FocusIn>', on_enter)
    user.bind("<FocusOut>", on_leave)

    tk.Frame(frame, width=295, height=2, bg="black").place(x=25, y=105)

    #####################################################################################
    def on_enter(e):
        code.delete(0, 'end')
        code.config(show='*')

    def on_leave(e):
        name = code.get()
        if name == "":
            code.insert(0, "Password")
            code.config(show='')

    def toggle_confirm_password():
        if code.cget('show') == "":
            code.config(show='*')
            show_button_confirm.config(text='Show')
        else:
            code.config(show='')
            show_button_confirm.config(text='Hide')

    code = tk.Entry(frame, width=20, show="", fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
    code.place(x=30, y=150)
    code.insert(0, "Password")
    code.bind('<FocusIn>', on_enter)
    code.bind("<FocusOut>", on_leave)

    show_button_confirm = tk.Button(frame, text='Show', command=toggle_confirm_password)
    show_button_confirm.place(x=280, y=150)

    tk.Frame(frame, width=295, height=2, bg="black").place(x=25, y=175)

    ########################################################################

    tk.Button(frame, width=10, pady=7, text="Sign in", bg="#57a1f8", fg="white", border=0, cursor="hand2",
              command=signin).place(x=65,
                                    y=204)

    tk.Button(frame, width=10, pady=7, text="Back", bg="#57a1f8", fg="white", border=0, cursor="hand2",
              command=Log_out).place(x=180,
                                     y=204)
    label = tk.Label(frame, text="Don't, have an account?", fg="black", bg="white",
                     font=("Microsoft YaHei UI Light", 9))
    label.place(x=75, y=270)

    ############################################
    # SIGN UP
    ############################################

    def sign_up():
        # Create a new window for Signup page
        window2 = tk.Toplevel(window)
        window2.title("SignUP")
        window2.geometry("1520x785+0+0")
        window2.config(bg="#fff")
        window2.resizable(False, False)

        # Add a photo for signup
        global img2
        img2 = tk.PhotoImage(file=r"D:\Pycharm\project testing\images\login2.png")
        tk.Label(window2, image=img2, border=0, bg="white").place(x=300, y=250)

        frame2 = tk.Frame(window2, width=565, height=500, bg="#fff")
        frame2.place(x=800, y=160)

        heading2 = tk.Label(frame2, text="Sign Up", fg="#57a1f8", bg="white",
                            font=("Microsoft YaHei UI Light", 23, "bold"))
        heading2.place(x=120, y=5)

        ####################################
        def validate_username(event):
            username = new_user.get()

            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            users = cursor.fetchone()
            if users:
                username_error.config(text="Username already exists")
                return
            elif not all(name.isalpha() or name.isspace() for name in username):
                username_error.config(text="Username must be alphabetic")
                return
            # Check if username is empty
            elif username == "":
                username_error.config(text="Username cannot be empty")
                return
            else:
                username_error.config(text="")  # Clear error message if all conditions are met
                return username

        def enter(e):
            new_user.delete(0, 'end')

        def leave(e):
            name = new_user.get()
            if name == "":
                new_user.insert(0, "Username")
                new_user.config(show='')

        new_user = tk.Entry(frame2, width=20, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        new_user.place(x=30, y=80)
        new_user.insert(0, "Username")
        new_user.bind('<FocusIn>', enter)
        new_user.bind("<FocusOut>", leave)
        new_user.bind("<KeyRelease>", validate_username)
        tk.Frame(frame2, width=295, height=2, bg="black").place(x=25, y=105)

        ######################################################

        def validate_wieght(event):
            wiegth = patient_weight.get()
            if not all(name.isdigit() or name.isspace() for name in wiegth):
                wiegth_error.config(text="wieght must be digit")
                return
            # Check if username is empty
            elif wiegth == "":
                wiegth_error.config(text="wieght cannot be empty")
                return
            else:
                wiegth_error.config(text="")  # Clear error message if all conditions are met
                return wiegth

        def enter(e):
            patient_weight.delete(0, 'end')

        def leave(e):
            name = patient_weight.get()
            if name == "":
                patient_weight.insert(0, "Patient Weight")
                patient_weight.config(show='')

        patient_weight = tk.Entry(frame2, width=20, fg="black", border=0, bg="white",
                                  font=("Microsoft YaHei UI Light", 11))
        patient_weight.place(x=30, y=150)
        patient_weight.insert(0, "Patient Weight")
        patient_weight.bind('<FocusIn>', enter)
        patient_weight.bind("<FocusOut>", leave)
        patient_weight.bind("<KeyRelease>", validate_wieght)
        tk.Frame(frame2, width=295, height=2, bg="black").place(x=25, y=175)

        #####################################################
        def validate_BP(event):
            bp = patient_bp.get()
            if not all(name.isdigit() or name.isspace() for name in bp):
                bp_error.config(text="BP must be digit")
                return
            # Check if username is empty
            elif bp == "":
                bp_error.config(text="BP cannot be empty")
                return
            else:
                bp_error.config(text="")  # Clear error message if all conditions are met
                return bp

        def enter(e):
            patient_bp.delete(0, 'end')

        def leave(e):
            name = patient_bp.get()
            if name == "":
                patient_bp.insert(0, "Patient Blood Pressure")
                patient_bp.config(show='')

        patient_bp = tk.Entry(frame2, width=20, fg="black", border=0, bg="white",
                              font=("Microsoft YaHei UI Light", 11))
        patient_bp.place(x=30, y=200)
        patient_bp.insert(0, "Blood Pressure")
        patient_bp.bind('<FocusIn>', enter)
        patient_bp.bind("<FocusOut>", leave)
        patient_bp.bind("<KeyRelease>", validate_BP)
        tk.Frame(frame2, width=295, height=2, bg="black").place(x=25, y=224)

        ######################################
        # Function to validate password strength
        def validate_password_strength(password):
            # Check password length
            if len(password) < 8:
                return "weak"
            if len(password) < 8:
                return "length"

            # Check for at least 2 digits, 2 alphabets, and 2 special characters
            digit_count = len(re.findall(r'\d', password))
            alpha_count = len(re.findall(r'[A-Za-z]', password))
            special_count = len(re.findall(r'[^\w\d\s]', password))

            if digit_count >= 2 and alpha_count >= 2 and special_count >= 2:
                return "strong"
            else:
                return "medium"

        def validate_password(event):
            password = new_code.get()
            password_error.config(text="")  # Clear error message if all conditions are met
            password_strength = validate_password_strength(password)
            if password == "":
                password_error.config(text="Password not be Empty", fg="red")
                return
            if not password[0].isalpha():
                password_error.config(text="Password must start with an alphabet")
                return
            if password_strength == "length":
                password_error.config(text="Password length must be 8 ", fg="red")
                return
            if password_strength == "weak":
                password_error.config(text="Password is too weak and length minimum be 8", fg="red")
                return
            if password_strength == "medium":
                password_error.config(text="Password strength is medium", fg="yellow")
                return
            if password_strength == "strong":
                password_error.config(text="Password strength is strong", fg="green")
                return password

        def enter(e):
            if new_code.get() == "Password":
                new_code.delete(0, 'end')
            new_code.config(show='*')

        def leave(e):
            if not new_code.get():
                new_code.insert(0, "Password")
                new_code.config(show='')
            else:
                new_code.config(show='*')

        def Hide_password():
            if new_code.cget('show') == "":
                new_code.config(show='*')
                show_button.config(text='Show')
            else:
                new_code.config(show='')
                show_button.config(text='Hide')

        new_code = tk.Entry(frame2, width=20, fg="black", show='', border=0, bg="white",
                            font=("Microsoft YaHei UI Light", 11))
        new_code.place(x=30, y=250)
        new_code.insert(0, "Password")
        new_code.bind("<FocusIn>", enter)
        new_code.bind("<FocusOut>", leave)
        new_code.bind("<KeyRelease>", validate_password)

        show_button = tk.Button(frame2, text='Show', border='0', command=Hide_password)
        show_button.place(x=280, y=250)
        pass_label = tk.Label(frame2, text='''  2 digit, 2 alphabet, 2 special character 
        are required in password''',
                              font=("Microsoft YaHei UI Light", 10), bg='#fff', justify='left')
        pass_label.place(x=320, y=240)

        tk.Frame(frame2, width=295, height=2, bg="black").place(x=25, y=275)

        #############################
        def validate_confirm_password(event):

            password = new_code.get()
            confirm_password = confirm_code.get()
            if confirm_password == "":
                confirm_error.config(text="Confirm Password not be Empty")
                return
            elif password != confirm_password:
                confirm_error.config(text="Password and Confirm password do not match")
                return
            else:
                confirm_error.config(text="")  # Clear error message if all conditions are met
                return True

        def enter(e):
            if confirm_code.get() == "Confirm Password":
                confirm_code.delete(0, 'end')
            confirm_code.config(show='*')

        def leave(e):
            if not confirm_code.get():
                confirm_code.insert(0, "Confirm Password")
                confirm_code.config(show='')
            else:
                confirm_code.config(show='*')

        def toggle_confirm_password():
            if confirm_code.cget('show') == "":
                confirm_code.config(show='*')
                show_button_confirm.config(text='Show')
            else:
                confirm_code.config(show='')
                show_button_confirm.config(text='Hide')

        confirm_code = tk.Entry(frame2, width=20, show='', fg="black", border=0, bg="white",
                                font=("Microsoft YaHei UI Light", 11))
        confirm_code.place(x=30, y=310)
        confirm_code.insert(0, "Confirm Password")
        confirm_code.bind("<FocusIn>", enter)
        confirm_code.bind("<FocusOut>", leave)
        confirm_code.bind("<KeyRelease>", validate_confirm_password)

        show_button_confirm = tk.Button(frame2, text='Show', command=toggle_confirm_password)
        show_button_confirm.place(x=280, y=310)

        tk.Frame(frame2, width=295, height=2, bg="black").place(x=25, y=338)

        ###############################################
        def signup(event):
            wieght_valid = validate_wieght(event)
            bp_valid = validate_BP(event)
            username_valid = validate_username(event)
            password_valid = validate_password(event)
            confirm_password_valid = validate_confirm_password(event)
            if wieght_valid is None:
                wiegth_error.config(text="enter the Patient Wieght")
            elif bp_valid is None:
                bp_error.config(text="enter the Patient Blood Pressure")
            elif username_valid == "Username":
                username_error.config(text="Enter the username")
            elif username_valid is None:
                username_error.config(text="Username already exits")
            elif password_valid is None:
                password_error.config(text="Password length must be 8")
            else:
                cursor.execute("INSERT INTO users(username, password, weight, Blood_pressure ) VALUES (?, ?, ?, ?)", (username_valid, password_valid,wieght_valid,bp_valid,))
                conn.commit()
                messagebox.showinfo("Success", "Sign up successful")
                window2.destroy()

        def sign():
            window2.destroy()

        # Create error labels
        username_error = tk.Label(frame2, text="", fg="red", bg="white")
        username_error.place(x=23, y=110)
        wiegth_error = tk.Label(frame2, text="", fg="red", bg="white")
        wiegth_error.place(x=23, y=180)
        bp_error = tk.Label(frame2, text="", fg="red", bg="white")
        bp_error.place(x=23, y=230)
        password_error = tk.Label(frame2, text="", fg="red", bg="white")
        password_error.place(x=23, y=280)
        confirm_error = tk.Label(frame2, text="", fg="red", bg="white")
        confirm_error.place(x=23, y=345)

        # Create a button for signup
        tk.Button(frame2, width=30, pady=7, text="Sign up", bg="#57a1f8", fg="black", border=0, cursor="hand2",
                  command=lambda event=None: signup(event)).place(x=65,
                                                                  y=385)
        label2 = tk.Label(frame2, text="I have an account?", fg="black", bg="white",
                          font=("Microsoft YaHei UI Light", 9))
        label2.place(x=75, y=420)

        sign_in = tk.Button(frame2, width=7, text="Sign in", border=0, fg="#57a1f8",
                            bg="white", cursor="hand2", command=sign)
        sign_in.place(x=182, y=420)

    sign_up = tk.Button(frame, width=7, text="Sign Up", border=0, fg="#57a1f8",
                        bg="white", cursor="hand2", command=sign_up)
    sign_up.place(x=212, y=270)
    window.mainloop()


