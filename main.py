from tkinter import Tk, Frame, Label, Entry, Button, Listbox, Scrollbar, messagebox, Toplevel, END, ANCHOR
from PIL import Image, ImageTk
import sqlite3

fonts = ('Courier New', 13, 'bold')
fonts1 = ('Courier New', 17, 'bold')

root = Tk()
root.iconbitmap(default="../assets/logo.ico")
root.title("WELCOME")
root.geometry('900x660+50+50')

def create_database():
    conn = sqlite3.connect('college_events.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS admins
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS event
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, event_name TEXT, event_time TEXT, event_venue TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS participant
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, event_name TEXT, participant_name TEXT)''')

    conn.commit()
    conn.close()

create_database()

class Home:
    def __init__(self, root):
        self.root = root
        self.root.title("HOME")
        self.page = Frame(self.root, width=800, height=600)
        self.page.place(relwidth=1, relheight=1)

        self.image = Image.open('../assets/bg2.jpg')
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = Label(self.page, image=self.image)
        self.image_label.place(relwidth=1, relheight=1)

        self.main_label = Label(self.page, text='WELCOME', font=('comic sans', 40, 'bold'), bg='gray36', fg='white')
        self.main_label.place(x=922, y=80)
        self.main_label2 = Label(self.page, text="CAMPUS EVENT SCHEDULER", font=('comic sans', 30, 'bold'), bg='gray36', fg='white')
        self.main_label2.place(x=800, y=200)
        self.main_label_btn = Button(self.page, text='ENTER', font=('comic sans', 25, 'bold'), bg='gray36', fg='white', command=self.home_login)
        self.main_label_btn.place(x=982, y=350)

    def home_login(self):
        self.page.destroy()
        home_obj = Main(root)


class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("LOGIN PAGE")
        self.right = Frame(self.root, width=900, height=700, bg='wheat3')
        self.right.place(relwidth=1, relheight=1)

        self.admin_logo = Image.open('../assets/administrator.png')
        self.admin_logo = self.admin_logo.resize((200, 200))
        self.admin_logo = ImageTk.PhotoImage(self.admin_logo)
        self.admin_logo_lbl = Label(self.right, image=self.admin_logo)
        self.admin_logo_lbl.place(x=100, y=30)

        self.admin__login = Label(self.right, text="Admin login")
        self.admin__login.place(x=200, y=225)
        self.admin_name = Label(self.right, text='USER ID', bg='steel blue', fg='white', font=fonts, width=9)
        self.admin_name.place(x=100, y=270)
        self.admin_name_entry = Entry(self.right, width=10, font=fonts)
        self.admin_name_entry.place(x=200, y=270)
        self.admin_pass = Label(self.right, text='PASSWORD', bg='steel blue', fg='white', font=fonts, width=9)
        self.admin_pass.place(x=100, y=300)
        self.admin_pass_entry = Entry(self.right, width=10, font=fonts, show='*')  # Password is hidden by default
        self.admin_pass_entry.place(x=200, y=300)

        self.admin_pass_show_btn = Button(self.right, text='Show Password', font=fonts, command=self.show_admin_password)
        self.admin_pass_show_btn.place(x=170, y=350)

        self.admin_login_btn = Button(self.right, text='LOGIN', font=fonts, command=self.admin_login)
        self.admin_login_btn.place(x=150, y=400)

        self.admin_sign_up_btn = Button(self.right, text='SIGN UP', font=fonts, command=self.admin_signup)
        self.admin_sign_up_btn.place(x=250, y=400)

        self.left = Frame(self.root, width=900, height=700, bg='wheat3')
        self.left.place(x=450, y=0)

        self.student_logo = Image.open('../assets/student.png')
        self.student_logo = self.student_logo.resize((200, 200))
        self.student_logo = ImageTk.PhotoImage(self.student_logo)
        self.student_logo_lbl = Label(self.left, image=self.student_logo)
        self.student_logo_lbl.place(x=100, y=30)

        self.student__login = Label(self.left, text="Student login")
        self.student__login.place(x=200, y=225)

        self.student_name = Label(self.left, text='USER ID', bg='steel blue', fg='white', font=fonts, width=9)
        self.student_name.place(x=100, y=270)
        self.student_name_entry = Entry(self.left, width=10, font=fonts)
        self.student_name_entry.place(x=200, y=270)

        self.student_pass = Label(self.left, text='PASSWORD', bg='steel blue', fg='white', font=fonts, width=9)
        self.student_pass.place(x=100, y=300)
        self.student_pass_entry = Entry(self.left, width=10, font=fonts, show='*')  # Password is hidden by default
        self.student_pass_entry.place(x=200, y=300)

        self.student_pass_show_btn = Button(self.left, text='Show Password', font=fonts, command=self.show_student_password)
        self.student_pass_show_btn.place(x=170, y=350)

        self.student_login_btn = Button(self.left, text='LOGIN', font=fonts, command=self.student_login)
        self.student_login_btn.place(x=150, y=400)

        self.student_sign_up_btn = Button(self.left, text='SIGN UP', font=fonts, command=self.student_signup)
        self.student_sign_up_btn.place(x=250, y=400)

        self.main_logout_btn = Button(self.left, text='BACK', font=fonts, command=self.Main_logout)
        self.main_logout_btn.place(x=820, y=650)

    def Main_logout(self):
        self.left.destroy()
        self.right.destroy()
        admin_obj = Home(root)

    def admin_login(self):
        self.a_name = self.admin_name_entry.get()
        self.a_pass = self.admin_pass_entry.get()
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (self.a_name, self.a_pass))
        admin_data = c.fetchone()
        if admin_data:
            messagebox.showinfo('SUCCESS', 'Admin logged in successfully')
            self.right.destroy()
            self.left.destroy()
            admin_obj = Admin(root)
        else:
            messagebox.showerror('ERROR', 'Invalid username or password')
        conn.close()

    def student_login(self):
        self.b_name = self.student_name_entry.get()
        self.b_pass = self.student_pass_entry.get()
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE username = ? AND password = ?", (self.b_name, self.b_pass))
        student_data = c.fetchone()
        if student_data:
            messagebox.showinfo('SUCCESS', 'Student logged in successfully')
            self.right.destroy()
            self.left.destroy()
            student_obj = Student(root)
        else:
            messagebox.showerror('ERROR', 'Invalid username or password')
        conn.close()

    def admin_signup(self):
        self.a_name = self.admin_name_entry.get()
        self.a_pass = self.admin_pass_entry.get()
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT * FROM admins WHERE username = ?", (self.a_name,))
        admin_data = c.fetchone()
        if admin_data:
            messagebox.showerror('ERROR', 'Username already exists')
        else:
            c.execute("INSERT INTO admins (username, password) VALUES (?, ?)", (self.a_name, self.a_pass))
            conn.commit()
            messagebox.showinfo('SUCCESS', 'Admin signed up successfully')
        conn.close()

    def student_signup(self):
        self.b_name = self.student_name_entry.get()
        self.b_pass = self.student_pass_entry.get()
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE username = ?", (self.b_name,))
        student_data = c.fetchone()
        if student_data:
            messagebox.showerror('ERROR', 'Username already exists')
        else:
            c.execute("INSERT INTO students (username, password) VALUES (?, ?)", (self.b_name, self.b_pass))
            conn.commit()
            messagebox.showinfo('SUCCESS', 'Student signed up successfully')
        conn.close()

    def show_admin_password(self):
        # Toggle password visibility for admin password entry
        current_state = self.admin_pass_entry.cget('show')
        if current_state == '*':
            self.admin_pass_entry.config(show='')
        else:
            self.admin_pass_entry.config(show='*')

    def show_student_password(self):
        # Toggle password visibility for student password entry
        current_state = self.student_pass_entry.cget('show')
        if current_state == '*':
            self.student_pass_entry.config(show='')
        else:
            self.student_pass_entry.config(show='*')

class Admin:
    def __init__(self, root):
        self.root = root
        self.root.title("ADMIN DASHBOARD")
        self.right = Frame(self.root, width=900, height=700)
        self.right.place(relwidth=1, relheight=1)

        self.image = Image.open('../assets/calendar1.jpg')
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = Label(self.right, image=self.image)
        self.image_label.place(relwidth=1, relheight=1)


        self.student__login = Label(self.right, text="EVENT LIST", bg='white', fg='black')
        self.student__login.place(x=170, y=10)

        self.event_list = Listbox(self.right, font=fonts, width=50, height=20)
        self.event_list.place(x=100, y=60)

        scrollbar = Scrollbar(self.right, orient="vertical", command=self.event_list.yview)
        scrollbar.place(x=600, y=70, height=420)

        self.event_list.config(yscrollcommand=scrollbar.set)

        self.populate_events()

        self.event_list.bind('<<ListboxSelect>>', self.show_participants)

        self.add_event_btn = Button(self.right, text='Add Event', font=fonts, command=self.add_event_window)
        self.add_event_btn.place(x=215, y=500)

        self.add_participant_btn = Button(self.right, text='Add Participant', font=fonts, command=self.add_participant_window)
        self.add_participant_btn.place(x=185, y=550)

        self.remove_participant_btn = Button(self.right, text='Remove Participant', font=fonts, command=self.remove_participant_window)
        self.remove_participant_btn.place(x=370, y=550)

        self.remove_event_btn = Button(self.right, text='Clear Events', font=fonts, command=self.remove_event_window)
        self.remove_event_btn.place(x=400, y=500)

        self.admin_logout_btn = Button(self.right, text='LOGOUT', font=fonts, command=self.admin_logout)
        self.admin_logout_btn.place(x=820, y=500)

    def populate_events(self):
        self.event_list.delete(0, END)  # Clear existing items in the list
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT * FROM event")
        events = c.fetchall()
        for event in events:
            self.event_list.insert(END, f"{event[1]} - {event[2]} - {event[3]}")
        conn.close()

    def show_participants(self, event):
        selected_event = self.event_list.get(self.event_list.curselection())
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT * FROM participant WHERE event_name = ?", (selected_event,))
        participants = c.fetchall()
        conn.close()
        if participants:
            messagebox.showinfo('Participants', '\n'.join([participant[2] for participant in participants]))
        else:
            messagebox.showinfo('Participants', 'No participants found for this event.')

    def add_event_window(self):
        self.add_event_window = Toplevel(self.root)
        self.add_event_window.title('Add Event')
        self.add_event_window.geometry('600x400')
        self.add_event_window.grab_set()

        self.event_name_label = Label(self.add_event_window, text='Event Name:', font=fonts)
        self.event_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.event_name_entry = Entry(self.add_event_window, font=fonts)
        self.event_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.event_time_label = Label(self.add_event_window, text='Event Time:', font=fonts)
        self.event_time_label.grid(row=1, column=0, padx=10, pady=10)
        self.event_time_entry = Entry(self.add_event_window, font=fonts)
        self.event_time_entry.grid(row=1, column=1, padx=10, pady=10)

        self.event_venue_label = Label(self.add_event_window, text='Event Venue:', font=fonts)
        self.event_venue_label.grid(row=2, column=0, padx=10, pady=10)
        self.event_venue_entry = Entry(self.add_event_window, font=fonts)
        self.event_venue_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_event_button = Button(self.add_event_window, text='Add Event', font=fonts, command=self.add_event)
        self.add_event_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def add_event(self):
        event_name = self.event_name_entry.get()
        event_time = self.event_time_entry.get()
        event_venue = self.event_venue_entry.get()

        if event_name and event_time and event_venue:
            conn = sqlite3.connect('college_events.db')
            c = conn.cursor()
            c.execute("INSERT INTO event (event_name, event_time, event_venue) VALUES (?, ?, ?)",(event_name, event_time, event_venue))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Event added successfully.')
            self.populate_events()
            self.add_event_window.destroy()
        else:
            messagebox.showerror('Error', 'Please fill in all fields.')

    def add_participant_window(self):
        selected_event = self.event_list.get(self.event_list.curselection())
        if not selected_event:
            messagebox.showerror('Error', 'Please select an event.')
            return

        self.add_participant_window = Toplevel(self.root)
        self.add_participant_window.title('Add Participant')
        self.add_participant_window.geometry('600x400')
        self.add_participant_window.grab_set()

        self.participant_name_label = Label(self.add_participant_window, text='Participant Name:', font=fonts)
        self.participant_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.participant_name_entry = Entry(self.add_participant_window, font=fonts)
        self.participant_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.add_participant_button = Button(self.add_participant_window, text='Add Participant', font=fonts, command=self.add_participant)
        self.add_participant_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def add_participant(self):
        selected_event = self.event_list.get(self.event_list.curselection())
        participant_name = self.participant_name_entry.get()

        if selected_event and participant_name:
            conn = sqlite3.connect('college_events.db')
            c = conn.cursor()
            c.execute("INSERT INTO participant (event_name, participant_name) VALUES (?, ?)",(selected_event, participant_name))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Participant added successfully.')
            self.add_participant_window.destroy()
        else:
            messagebox.showerror('Error', 'Please fill in all fields.')

    def remove_participant_window(self):
        selected_event = self.event_list.get(self.event_list.curselection())
        if not selected_event:
            messagebox.showerror('Error', 'Please select an event.')
            return

        self.remove_participant_window = Toplevel(self.root)
        self.remove_participant_window.title('Remove Participant')
        self.remove_participant_window.geometry('600x400')
        self.remove_participant_window.grab_set()

        self.participant_name_label = Label(self.remove_participant_window, text='Participant Name:', font=fonts)
        self.participant_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.participant_name_entry = Entry(self.remove_participant_window, font=fonts)
        self.participant_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.remove_participant_button = Button(self.remove_participant_window, text='Remove Participant', font=fonts, command=self.remove_participant)
        self.remove_participant_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def remove_participant(self):
        selected_event = self.event_list.get(self.event_list.curselection())
        participant_name = self.participant_name_entry.get()

        if selected_event and participant_name:
            conn = sqlite3.connect('college_events.db')
            c = conn.cursor()
            c.execute("DELETE FROM participant WHERE event_name = ? AND participant_name = ?",(selected_event, participant_name))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Participant removed successfully.')
            self.remove_participant_window.destroy()
        else:
            messagebox.showerror('Error', 'Please fill in all fields.')

    def remove_event_window(self):
        selected_event = self.event_list.get(self.event_list.curselection())
        if not selected_event:
            messagebox.showerror('Error', 'Please select an event.')
            return

        self.remove_event_window = Toplevel(self.root)
        self.remove_event_window.title('Remove Event')
        self.remove_event_window.geometry('600x400')
        self.remove_event_window.grab_set()

        self.confirm_label = Label(self.remove_event_window, text=f'Are you sure you want to remove {selected_event}?', font=fonts)
        self.confirm_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.remove_event_button = Button(self.remove_event_window, text='Confirm', font=fonts, command=lambda: self.remove_event(selected_event))
        self.remove_event_button.grid(row=1, column=0, padx=10, pady=10)

        self.cancel_button = Button(self.remove_event_window, text='Cancel', font=fonts, command=self.remove_event_window.destroy)
        self.cancel_button.grid(row=1, column=1, padx=10, pady=10)

    def remove_event(self, selected_event):
        selected_event_index = self.event_list.curselection()
        if selected_event_index:
            selected_event = self.event_list.get(selected_event_index)
            conn = sqlite3.connect('college_events.db')
            c = conn.cursor()
            c.execute("DELETE FROM event WHERE event_name = ?", (selected_event,))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'Event removed successfully.')
            
            # Update the event list after deleting the event from the database
            self.populate_events()  # Update the event list
            self.event_list.delete(ANCHOR)  # Delete the selected item from the listbox
            self.remove_event_window.destroy()
        else:
            messagebox.showerror('Error', 'Please select an event to remove.')

    def admin_logout(self):
        self.right.destroy()
        admin_obj = Main(root)


class Student:
    def __init__(self, root):
        self.root = root
        self.root.title("STUDENT DASHBOARD")
        self.right = Frame(self.root, width=900, height=700)
        self.right.place(relwidth=1, relheight=1)

        self.image = Image.open('../assets/calendar1.jpg')
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = Label(self.right, image=self.image)
        self.image_label.place(relwidth=1, relheight=1)

        self.student__login = Label(self.right, text="EVENT LIST", bg='white', fg='black')
        self.student__login.place(x=170, y=10)

        self.event_list = Listbox(self.right, font=fonts, width=50, height=20)
        self.event_list.place(x=100, y=60)

        scrollbar = Scrollbar(self.right, orient="vertical", command=self.event_list.yview)
        scrollbar.place(x=600, y=70, height=420)

        self.event_list.config(yscrollcommand=scrollbar.set)

        self.event_list.bind('<<ListboxSelect>>', self.show_participants)
        self.populate_events()

        self.student_logout_btn = Button(self.right, text='LOGOUT', font=fonts, command=self.student_logout)
        self.student_logout_btn.place(x=820, y=500)

    def populate_events(self):
        self.event_list.delete(0, END)
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT * FROM event")
        events = c.fetchall()
        for event in events:
            self.event_list.insert('end', f"{event[1]} - {event[2]} - {event[3]}")
        conn.close()

    def show_participants(self, event):
        selected_event = self.event_list.get(self.event_list.curselection())
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT * FROM participant WHERE event_name = ?", (selected_event,))
        participants = c.fetchall()
        conn.close()
        if participants:
            messagebox.showinfo('Participants', '\n'.join([participant[2] for participant in participants]))
        else:
            messagebox.showinfo('Participants', 'No participants found for this event.')

    def student_logout(self):
        self.right.destroy()
        student_obj = Main(root)

home_obj = Home(root)
root.mainloop()
