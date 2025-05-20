from tkinter import Tk, Frame, Label, Entry, Button, Listbox, Scrollbar, messagebox, Toplevel, END, ANCHOR, Text, StringVar, LabelFrame, Radiobutton, Canvas
from PIL import Image, ImageTk
import sqlite3
import tkinter.ttk as ttk
from tkinter.ttk import Separator
import threading
import time

fonts = ('Courier New', 13, 'bold')
fonts1 = ('Courier New', 17, 'bold')

root = Tk()
root.iconbitmap(default="assets/logo.ico")
root.title("WELCOME")
root.geometry('900x660+50+50')

def create_database():
    conn = sqlite3.connect('college_events.db')
    c = conn.cursor()

    # Drop existing tables to ensure clean state
    c.execute("DROP TABLE IF EXISTS notifications")
    c.execute("DROP TABLE IF EXISTS attendance")
    c.execute("DROP TABLE IF EXISTS event_history")
    c.execute("DROP TABLE IF EXISTS event_templates")
    c.execute("DROP TABLE IF EXISTS event")
    c.execute("DROP TABLE IF EXISTS students")
    c.execute("DROP TABLE IF EXISTS admins")

    # Create tables with improved structure
    c.execute('''CREATE TABLE IF NOT EXISTS admins
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE,
                  password TEXT,
                  email TEXT UNIQUE,
                  full_name TEXT,
                  role TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE,
                  password TEXT,
                  email TEXT UNIQUE,
                  full_name TEXT,
                  student_id TEXT UNIQUE,
                  department TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Create event table with status column
    c.execute('''CREATE TABLE IF NOT EXISTS event
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  event_name TEXT,
                  event_time TEXT,
                  event_venue TEXT,
                  description TEXT,
                  requirements TEXT,
                  status TEXT DEFAULT 'Upcoming',
                  created_by INTEGER,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (created_by) REFERENCES admins(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS event_templates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  template_name TEXT,
                  description TEXT,
                  requirements TEXT,
                  created_by INTEGER,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (created_by) REFERENCES admins(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS event_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  event_id INTEGER,
                  action TEXT,
                  changed_by INTEGER,
                  changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (event_id) REFERENCES event(id),
                  FOREIGN KEY (changed_by) REFERENCES admins(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  event_id INTEGER,
                  user_id INTEGER,
                  user_type TEXT,
                  status TEXT,
                  attended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (event_id) REFERENCES event(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS notifications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  user_type TEXT,
                  event_id INTEGER,
                  message TEXT,
                  is_read BOOLEAN DEFAULT 0,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (event_id) REFERENCES event(id))''')

    # Check if default admin exists
    c.execute("SELECT * FROM admins WHERE username = 'admin'")
    if not c.fetchone():
        # Create default admin account
        c.execute("""INSERT INTO admins 
                    (username, password, email, full_name, role)
                    VALUES (?, ?, ?, ?, ?)""",
                 ('admin', 'admin123', 'admin@college.edu', 'System Administrator', 'super_admin'))

    conn.commit()
    conn.close()

create_database()


class Home:
    def __init__(self, root):
        self.root = root
        self.root.title("CAMPUS EVENT SCHEDULER")
        self.page = Frame(self.root, width=800, height=600)
        self.page.place(relwidth=1, relheight=1)

        # Load and set background image
        self.image = Image.open('assets/bg2.jpg')
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = Label(self.page, image=self.image)
        self.image_label.place(relwidth=1, relheight=1)

        # Welcome text with modern styling
        self.welcome_frame = Frame(self.page, bg='#333333')  # Dark gray background
        self.welcome_frame.place(relx=0.5, rely=0.5, anchor='center', width=600, height=400)

        self.main_label = Label(self.welcome_frame, 
                              text='WELCOME TO', 
                              font=('Helvetica', 40, 'bold'),
                              bg='#333333',
                              fg='white')
        self.main_label.place(relx=0.5, rely=0.2, anchor='center')

        self.main_label2 = Label(self.welcome_frame,
                               text="CAMPUS EVENT SCHEDULER",
                               font=('Helvetica', 30, 'bold'),
                               bg='#333333',
                               fg='white')
        self.main_label2.place(relx=0.5, rely=0.35, anchor='center')

        # Description
        self.description = Label(self.welcome_frame,
                               text="Your one-stop solution for managing and participating in campus events",
                               font=('Helvetica', 14),
                               bg='#333333',
                               fg='white',
                               wraplength=500)
        self.description.place(relx=0.5, rely=0.5, anchor='center')

        # Enter button with hover effect
        self.main_label_btn = Button(self.welcome_frame,
                                   text='ENTER',
                                   font=('Helvetica', 20, 'bold'),
                                   bg='#4a90e2',
                                   fg='white',
                                   command=self.home_login,
                                   width=15,
                                   cursor='hand2')
        self.main_label_btn.place(relx=0.5, rely=0.7, anchor='center')

        # Add hover effect
        def on_enter(e):
            self.main_label_btn['bg'] = '#357abd'

        def on_leave(e):
            self.main_label_btn['bg'] = '#4a90e2'

        self.main_label_btn.bind("<Enter>", on_enter)
        self.main_label_btn.bind("<Leave>", on_leave)

    def home_login(self):
        self.page.destroy()
        home_obj = Main(root)


class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("LOGIN PAGE")
        self.right = Frame(self.root, width=900, height=700, bg='wheat3')
        self.right.place(relwidth=1, relheight=1)

        # Admin section
        self.admin_logo = Image.open('assets/administrator.png')
        self.admin_logo = self.admin_logo.resize((200, 200))
        self.admin_logo = ImageTk.PhotoImage(self.admin_logo)
        self.admin_logo_lbl = Label(self.right, image=self.admin_logo)
        self.admin_logo_lbl.place(x=100, y=30)

        self.admin__login = Label(self.right, text="Admin login", font=('Helvetica', 14, 'bold'))
        self.admin__login.place(x=200, y=225)
        
        # Admin login fields
        self.admin_name = Label(self.right, text='USERNAME', bg='steel blue', fg='white', font=fonts, width=9)
        self.admin_name.place(x=100, y=270)
        self.admin_name_entry = Entry(self.right, width=20, font=fonts)
        self.admin_name_entry.place(x=200, y=270)
        
        self.admin_pass = Label(self.right, text='PASSWORD', bg='steel blue', fg='white', font=fonts, width=9)
        self.admin_pass.place(x=100, y=300)
        self.admin_pass_entry = Entry(self.right, width=20, font=fonts, show='*')
        self.admin_pass_entry.place(x=200, y=300)

        self.admin_pass_show_btn = Button(self.right, text='Show Password', font=fonts, command=self.show_admin_password)
        self.admin_pass_show_btn.place(x=170, y=350)

        self.admin_login_btn = Button(self.right, text='LOGIN', font=fonts, command=self.admin_login)
        self.admin_login_btn.place(x=150, y=400)

        # Student section
        self.left = Frame(self.root, width=900, height=700, bg='wheat3')
        self.left.place(x=450, y=0)

        self.student_logo = Image.open('assets/student.png')
        self.student_logo = self.student_logo.resize((200, 200))
        self.student_logo = ImageTk.PhotoImage(self.student_logo)
        self.student_logo_lbl = Label(self.left, image=self.student_logo)
        self.student_logo_lbl.place(x=100, y=30)

        self.student__login = Label(self.left, text="Student login", font=('Helvetica', 14, 'bold'))
        self.student__login.place(x=200, y=225)

        # Student login fields
        self.student_name = Label(self.left, text='USERNAME', bg='steel blue', fg='white', font=fonts, width=9)
        self.student_name.place(x=100, y=270)
        self.student_name_entry = Entry(self.left, width=20, font=fonts)
        self.student_name_entry.place(x=200, y=270)

        self.student_pass = Label(self.left, text='PASSWORD', bg='steel blue', fg='white', font=fonts, width=9)
        self.student_pass.place(x=100, y=300)
        self.student_pass_entry = Entry(self.left, width=20, font=fonts, show='*')
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
        username = self.admin_name_entry.get()
        password = self.admin_pass_entry.get()
        
        if not username or not password:
            messagebox.showerror('ERROR', 'Please fill in all fields')
            return
            
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
        admin_data = c.fetchone()
        
        if admin_data:
            messagebox.showinfo('SUCCESS', f'Welcome, {admin_data[4]}!')
            self.right.destroy()
            self.left.destroy()
            admin_obj = Admin(root, admin_data[0])  # Pass admin ID
        else:
            messagebox.showerror('ERROR', 'Invalid username or password')
        conn.close()

    def student_login(self):
        username = self.student_name_entry.get()
        password = self.student_pass_entry.get()
        
        if not username or not password:
            messagebox.showerror('ERROR', 'Please fill in all fields')
            return
            
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE username = ? AND password = ?", (username, password))
        student_data = c.fetchone()
        
        if student_data:
            messagebox.showinfo('SUCCESS', f'Welcome, {student_data[4]}!')
            self.right.destroy()
            self.left.destroy()
            student_obj = Student(root, student_data[0])  # Pass student ID
        else:
            messagebox.showerror('ERROR', 'Invalid username or password')
        conn.close()

    def student_signup(self):
        # Create signup window
        signup_window = Toplevel(self.root)
        signup_window.title('Student Registration')
        signup_window.geometry('500x600')
        signup_window.grab_set()

        # Form fields
        fields = [
            ('Username:', 'username'),
            ('Password:', 'password'),
            ('Email:', 'email'),
            ('Full Name:', 'full_name'),
            ('Student ID:', 'student_id'),
            ('Department:', 'department')
        ]

        entries = {}
        for i, (label, field) in enumerate(fields):
            Label(signup_window,
                  text=label,
                  font=fonts).grid(row=i, column=0, padx=10, pady=10)
            
            if field == 'password':
                entry = Entry(signup_window, width=30, font=fonts, show='*')
            else:
                entry = Entry(signup_window, width=30, font=fonts)
            
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[field] = entry

        def register():
            # Get values
            values = {field: entry.get() for field, entry in entries.items()}
            
            # Validate
            if not all(values.values()):
                messagebox.showerror('Error', 'Please fill in all fields')
                return
                
            # Check if username or email already exists
            conn = sqlite3.connect('college_events.db')
            c = conn.cursor()
            
            c.execute("SELECT * FROM students WHERE username = ? OR email = ? OR student_id = ?",
                     (values['username'], values['email'], values['student_id']))
            if c.fetchone():
                messagebox.showerror('Error', 'Username, email, or student ID already exists')
                conn.close()
                return
            
            # Insert new student
            c.execute("""INSERT INTO students 
                        (username, password, email, full_name, student_id, department)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                     (values['username'], values['password'], values['email'],
                      values['full_name'], values['student_id'], values['department']))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo('Success', 'Registration successful! Please login.')
            signup_window.destroy()

        Button(signup_window,
               text='Register',
               font=fonts,
               command=register).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def show_admin_password(self):
        current_state = self.admin_pass_entry.cget('show')
        self.admin_pass_entry.config(show='' if current_state == '*' else '*')

    def show_student_password(self):
        current_state = self.student_pass_entry.cget('show')
        self.student_pass_entry.config(show='' if current_state == '*' else '*')


class Admin:
    def __init__(self, root, admin_id):
        self.root = root
        self.admin_id = admin_id
        self.root.title("ADMIN DASHBOARD")
        
        # Make window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.right = Frame(self.root)
        self.right.grid(row=0, column=0, sticky='nsew')
        self.right.grid_rowconfigure(1, weight=1)
        self.right.grid_columnconfigure(1, weight=1)

        # Modern styling
        self.style = {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'button_bg': '#4a90e2',
            'button_fg': 'white',
            'font': ('Helvetica', 12),
            'title_font': ('Helvetica', 16, 'bold')
        }

        # Main container
        self.main_container = Frame(self.right, bg=self.style['bg'])
        self.main_container.grid(row=0, column=0, sticky='nsew')
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        # Header
        self.header = Frame(self.main_container, bg=self.style['button_bg'], height=60)
        self.header.grid(row=0, column=0, columnspan=2, sticky='ew')
        
        # Get admin name with loading indicator
        def get_admin_name():
            conn = sqlite3.connect('college_events.db')
            c = conn.cursor()
            c.execute("SELECT full_name FROM admins WHERE id = ?", (self.admin_id,))
            admin_name = c.fetchone()[0]
            conn.close()
            return admin_name
            
        show_loading(self.header, get_admin_name)
        
        self.title_label = Label(self.header, 
                               text="Loading...", 
                               font=self.style['title_font'],
                               bg=self.style['button_bg'],
                               fg='white')
        self.title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Update title after loading
        def update_title():
            admin_name = get_admin_name()
            self.title_label.config(text=f"Welcome, {admin_name}")
            
        self.root.after(100, update_title)

        # Navigation buttons
        self.nav_frame = Frame(self.main_container, bg=self.style['bg'])
        self.nav_frame.grid(row=1, column=0, sticky='ns', padx=20, pady=20)

        self.buttons = [
            ("Events", self.show_events)
        ]

        for i, (text, command) in enumerate(self.buttons):
            btn = Button(self.nav_frame, 
                        text=text,
                        font=self.style['font'],
                        bg=self.style['button_bg'],
                        fg='white',
                        command=command)
            btn.grid(row=i, column=0, pady=5, sticky='ew')

        # Main content area
        self.content_frame = Frame(self.main_container, bg='white')
        self.content_frame.grid(row=1, column=1, sticky='nsew', padx=20, pady=20)

        # Show events by default
        self.show_events()

        # Logout button
        self.logout_btn = Button(self.main_container,
                               text='LOGOUT',
                               font=self.style['font'],
                               bg='#e74c3c',
                               fg='white',
                               command=self.admin_logout)
        self.logout_btn.grid(row=0, column=1, sticky='e', padx=20, pady=10)

    def show_events(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Add event button
        add_btn = Button(self.content_frame,
                        text='Add New Event',
                        font=self.style['font'],
                        bg=self.style['button_bg'],
                        fg='white',
                        command=self.add_event_window)
        add_btn.grid(row=0, column=0, sticky='w', pady=10)

        # Event list with status
        self.event_list = Listbox(self.content_frame,
                                 font=self.style['font'],
                                 width=70,
                                 height=20)
        self.event_list.grid(row=1, column=0, sticky='nsew', pady=10)

        scrollbar = Scrollbar(self.content_frame,
                            orient="vertical",
                            command=self.event_list.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')

        self.event_list.config(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Show loading while populating events
        def populate():
            self.populate_events()
            
        show_loading(self.content_frame, populate)
        self.event_list.bind('<<ListboxSelect>>', self.show_event_details)

    def populate_events(self):
        self.event_list.delete(0, END)
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT id, event_name, event_time, event_venue, status FROM event ORDER BY event_time")
        events = c.fetchall()
        for event in events:
            status_color = {
                'Upcoming': 'blue',
                'Ongoing': 'green',
                'Completed': 'gray'
            }.get(event[4], 'black')
            
            self.event_list.insert('end', f"{event[1]} - {event[2]} - {event[3]} [{event[4]}]")
            self.event_list.itemconfig('end', fg=status_color)
        conn.close()

    def add_event_window(self):
        self.add_event_window = Toplevel(self.root)
        self.add_event_window.title('Add Event')
        self.add_event_window.geometry('600x700')
        self.add_event_window.grab_set()

        # Form fields
        fields = [
            ('Event Name:', 'event_name'),
            ('Event Time:', 'event_time'),
            ('Event Venue:', 'event_venue'),
            ('Description:', 'description'),
            ('Requirements:', 'requirements'),
            ('Status:', 'status')
        ]

        self.entries = {}
        for i, (label, field) in enumerate(fields):
            Label(self.add_event_window,
                  text=label,
                  font=self.style['font']).grid(row=i, column=0, padx=10, pady=10)
            
            if field == 'status':
                # Status dropdown
                self.entries[field] = ttk.Combobox(self.add_event_window,
                                                 values=['Upcoming', 'Ongoing', 'Completed'],
                                                 state='readonly')
                self.entries[field].set('Upcoming')
            elif field in ['description', 'requirements']:
                # Text areas for longer content
                self.entries[field] = Text(self.add_event_window,
                                         height=4,
                                         width=40)
            else:
                # Regular entry fields
                self.entries[field] = Entry(self.add_event_window,
                                          width=40,
                                          font=self.style['font'])

            self.entries[field].grid(row=i, column=1, padx=10, pady=10)

        # Add event button
        Button(self.add_event_window,
               text='Add Event',
               font=self.style['font'],
               bg=self.style['button_bg'],
               fg='white',
               command=self.add_event).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def add_event(self):
        # Get values from entries
        values = {field: entry.get() if not isinstance(entry, Text) else entry.get('1.0', 'end-1c')
                 for field, entry in self.entries.items()}

        if all(values.values()):
            conn = sqlite3.connect('college_events.db')
            c = conn.cursor()
            
            # Insert event
            c.execute("""INSERT INTO event 
                        (event_name, event_time, event_venue, description, requirements, status)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                     (values['event_name'], values['event_time'], values['event_venue'],
                      values['description'], values['requirements'], values['status']))
            
            event_id = c.lastrowid
            
            # Add to event history
            c.execute("""INSERT INTO event_history 
                        (event_id, action, changed_by)
                        VALUES (?, ?, ?)""",
                     (event_id, 'Created', self.admin_id))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo('Success', 'Event added successfully.')
            self.add_event_window.destroy()
            self.show_events()
        else:
            messagebox.showerror('Error', 'Please fill in all fields.')

    def show_event_details(self, event):
        selected_index = self.event_list.curselection()
        if not selected_index:
            return

        selected_event = self.event_list.get(selected_index)
        event_name = selected_event.split(' - ')[0]
        
        # Show event details in a new window
        details_window = Toplevel(self.root)
        details_window.title('Event Details')
        details_window.geometry('900x800')
        details_window.configure(bg='#f0f0f0')
        
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM event WHERE event_name = ?""", (event_name,))
        event = c.fetchone()
        
        if event:
            # Create main frame with padding
            main_frame = Frame(details_window, bg='#f0f0f0', padx=30, pady=30)
            main_frame.pack(fill='both', expand=True)
            
            # Header with event name
            header_frame = Frame(main_frame, bg='#4a90e2', pady=20)
            header_frame.pack(fill='x', pady=(0, 20))
            
            Label(header_frame,
                  text=event[1],
                  font=('Helvetica', 24, 'bold'),
                  bg='#4a90e2',
                  fg='white').pack()
            
            # Event details section
            details_frame = LabelFrame(main_frame,
                                     text="Event Information",
                                     font=('Helvetica', 12, 'bold'),
                                     bg='white',
                                     padx=20,
                                     pady=20)
            details_frame.pack(fill='x', pady=(0, 20))
            
            # Display event details in a grid
            fields = [
                ('Time:', event[2]),
                ('Venue:', event[3]),
                ('Description:', event[4]),
                ('Requirements:', event[5])
            ]
            
            for i, (label, value) in enumerate(fields):
                # Label frame for each field
                field_frame = Frame(details_frame, bg='white')
                field_frame.pack(fill='x', pady=5)
                
                Label(field_frame,
                      text=label,
                      font=('Helvetica', 11, 'bold'),
                      bg='white',
                      width=15,
                      anchor='w').pack(side='left', padx=(0, 10))
                
                Label(field_frame,
                      text=value,
                      font=('Helvetica', 11),
                      bg='white',
                      wraplength=600,
                      justify='left').pack(side='left', fill='x', expand=True)
            
            # Registrations section
            registrations_frame = LabelFrame(main_frame,
                                          text="Registered Students",
                                          font=('Helvetica', 12, 'bold'),
                                          bg='white',
                                          padx=20,
                                          pady=20)
            registrations_frame.pack(fill='both', expand=True, pady=(0, 20))
            
            # Header with registration count
            c.execute("""
                SELECT COUNT(*) FROM attendance 
                WHERE event_id = ? AND user_type = 'student'
            """, (event[0],))
            reg_count = c.fetchone()[0]
            
            count_frame = Frame(registrations_frame, bg='white')
            count_frame.pack(fill='x', pady=(0, 10))
            
            Label(count_frame,
                  text=f"Total Registrations: {reg_count}",
                  font=('Helvetica', 11, 'bold'),
                  bg='white').pack(side='left')
            
            # Create Treeview for registrations with custom style
            style = ttk.Style()
            style.configure("Custom.Treeview",
                          background="white",
                          foreground="black",
                          rowheight=25,
                          fieldbackground="white")
            style.configure("Custom.Treeview.Heading",
                          font=('Helvetica', 10, 'bold'))
            
            columns = ('Student ID', 'Name', 'Department', 'Registration Date')
            registrations_tree = ttk.Treeview(registrations_frame,
                                           columns=columns,
                                           show='headings',
                                           style="Custom.Treeview")
            
            # Set column headings and widths
            column_widths = {
                'Student ID': 100,
                'Name': 200,
                'Department': 150,
                'Registration Date': 150
            }
            
            for col in columns:
                registrations_tree.heading(col, text=col)
                registrations_tree.column(col, width=column_widths[col], anchor='center')
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(registrations_frame,
                                    orient="vertical",
                                    command=registrations_tree.yview)
            registrations_tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack the treeview and scrollbar
            registrations_tree.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Get registered students
            c.execute("""
                SELECT s.student_id, s.full_name, s.department, a.attended_at
                FROM attendance a
                JOIN students s ON a.user_id = s.id
                WHERE a.event_id = ? AND a.user_type = 'student'
                ORDER BY a.attended_at DESC
            """, (event[0],))
            
            registrations = c.fetchall()
            for reg in registrations:
                registrations_tree.insert('', 'end', values=reg)
            
            # Export button with modern styling
            def export_registrations():
                try:
                    filename = f'registrations_{event[1]}.txt'
                    with open(filename, 'w') as f:
                        f.write(f"Event: {event[1]}\n")
                        f.write(f"Time: {event[2]}\n")
                        f.write(f"Venue: {event[3]}\n")
                        f.write(f"Total Registrations: {len(registrations)}\n\n")
                        f.write("Registered Students:\n")
                        f.write("-" * 80 + "\n")
                        for reg in registrations:
                            f.write(f"Student ID: {reg[0]}\n")
                            f.write(f"Name: {reg[1]}\n")
                            f.write(f"Department: {reg[2]}\n")
                            f.write(f"Registration Date: {reg[3]}\n")
                            f.write("-" * 80 + "\n")
                    messagebox.showinfo('Success', f'Registrations exported to {filename}')
                except Exception as e:
                    messagebox.showerror('Error', f'Failed to export registrations: {str(e)}')
            
            button_frame = Frame(main_frame, bg='#f0f0f0')
            button_frame.pack(fill='x', pady=(0, 10))
            
            export_btn = Button(button_frame,
                              text='Export Registrations',
                              font=('Helvetica', 11, 'bold'),
                              bg='#4a90e2',
                              fg='white',
                              padx=20,
                              pady=10,
                              command=export_registrations)
            export_btn.pack(side='right')
            
            # Add hover effect
            def on_enter(e):
                export_btn['bg'] = '#357abd'
            
            def on_leave(e):
                export_btn['bg'] = '#4a90e2'
            
            export_btn.bind("<Enter>", on_enter)
            export_btn.bind("<Leave>", on_leave)
        
        conn.close()

    def admin_logout(self):
        self.right.destroy()
        admin_obj = Main(root)


class Student:
    def __init__(self, root, student_id):
        self.root = root
        self.student_id = student_id
        self.root.title("STUDENT DASHBOARD")
        
        # Make window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.right = Frame(self.root)
        self.right.grid(row=0, column=0, sticky='nsew')
        self.right.grid_rowconfigure(1, weight=1)
        self.right.grid_columnconfigure(1, weight=1)

        # Modern styling
        self.style = {
            'bg': '#f0f0f0',
            'fg': '#333333',
            'button_bg': '#4a90e2',
            'button_fg': 'white',
            'font': ('Helvetica', 12),
            'title_font': ('Helvetica', 16, 'bold')
        }

        # Main container
        self.main_container = Frame(self.right, bg=self.style['bg'])
        self.main_container.grid(row=0, column=0, sticky='nsew')
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        # Header
        self.header = Frame(self.main_container, bg=self.style['button_bg'], height=60)
        self.header.grid(row=0, column=0, columnspan=2, sticky='ew')
        
        # Get student name with loading indicator
        def get_student_name():
            conn = sqlite3.connect('college_events.db')
            c = conn.cursor()
            c.execute("SELECT full_name FROM students WHERE id = ?", (self.student_id,))
            student_name = c.fetchone()[0]
            conn.close()
            return student_name
            
        show_loading(self.header, get_student_name)
        
        self.title_label = Label(self.header, 
                               text="Loading...", 
                               font=self.style['title_font'],
                               bg=self.style['button_bg'],
                               fg='white')
        self.title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Update title after loading
        def update_title():
            student_name = get_student_name()
            self.title_label.config(text=f"Welcome, {student_name}")
            
        self.root.after(100, update_title)

        # Navigation buttons
        self.nav_frame = Frame(self.main_container, bg=self.style['bg'])
        self.nav_frame.grid(row=1, column=0, sticky='ns', padx=20, pady=20)

        self.buttons = [
            ("Events", self.show_events),
            ("My Events", self.show_my_events)
        ]

        for i, (text, command) in enumerate(self.buttons):
            btn = Button(self.nav_frame, 
                        text=text,
                        font=self.style['font'],
                        bg=self.style['button_bg'],
                        fg='white',
                        command=command)
            btn.grid(row=i, column=0, pady=5, sticky='ew')

        # Main content area
        self.content_frame = Frame(self.main_container, bg='white')
        self.content_frame.grid(row=1, column=1, sticky='nsew', padx=20, pady=20)

        # Show events by default
        self.show_events()

        # Logout button
        self.logout_btn = Button(self.main_container,
                               text='LOGOUT',
                               font=self.style['font'],
                               bg='#e74c3c',
                               fg='white',
                               command=self.student_logout)
        self.logout_btn.grid(row=0, column=1, sticky='e', padx=20, pady=10)

    def show_events(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Event list with status
        self.event_list = Listbox(self.content_frame,
                                 font=self.style['font'],
                                 width=70,
                                 height=20)
        self.event_list.grid(row=0, column=0, sticky='nsew', pady=10)

        scrollbar = Scrollbar(self.content_frame,
                            orient="vertical",
                            command=self.event_list.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.event_list.config(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Show loading while populating events
        def populate():
            self.populate_events()
            
        show_loading(self.content_frame, populate)
        self.event_list.bind('<<ListboxSelect>>', self.show_event_details)

    def populate_events(self):
        self.event_list.delete(0, END)
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("SELECT id, event_name, event_time, event_venue, status FROM event ORDER BY event_time")
        events = c.fetchall()
        for event in events:
            status_color = {
                'Upcoming': 'blue',
                'Ongoing': 'green',
                'Completed': 'gray'
            }.get(event[4], 'black')
            
            self.event_list.insert('end', f"{event[1]} - {event[2]} - {event[3]} [{event[4]}]")
            self.event_list.itemconfig('end', fg=status_color)
        conn.close()

    def show_event_details(self, event):
        selected_index = self.event_list.curselection()
        if not selected_index:
            return
            
        selected_event = self.event_list.get(selected_index)
        event_name = selected_event.split(' - ')[0]
        
        # Show event details in a new window
        details_window = Toplevel(self.root)
        details_window.title('Event Details')
        details_window.geometry('600x600')
        
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM event WHERE event_name = ?""", (event_name,))
        event = c.fetchone()
        
        if event:
            # Create main frame with padding
            main_frame = Frame(details_window, padx=20, pady=20)
            main_frame.pack(fill='both', expand=True)
            
            # Event details section
            details_frame = LabelFrame(main_frame, text="Event Information", padx=10, pady=10)
            details_frame.pack(fill='x', pady=(0, 20))
            
            # Display event details
            fields = [
                ('Event Name:', event[1]),
                ('Time:', event[2]),
                ('Venue:', event[3]),
                ('Description:', event[4]),
                ('Requirements:', event[5]),
                ('Status:', event[6])
            ]
            
            for i, (label, value) in enumerate(fields):
                Label(details_frame,
                      text=label,
                      font=self.style['font'],
                      width=15,
                      anchor='w').grid(row=i, column=0, padx=5, pady=5, sticky='w')
                Label(details_frame,
                      text=value,
                      font=self.style['font'],
                      wraplength=400).grid(row=i, column=1, padx=5, pady=5, sticky='w')
            
            # Register button for upcoming events
            if event[6] == 'Upcoming':
                Button(main_frame,
                      text='Register for Event',
                      font=self.style['font'],
                      bg=self.style['button_bg'],
                      fg='white',
                      command=lambda: self.register_for_event(event[0])).pack(pady=10)
        
        conn.close()

    def register_for_event(self, event_id):
        # Add attendance record
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("""INSERT INTO attendance 
                    (event_id, user_id, user_type, status)
                    VALUES (?, ?, ?, ?)""",
                 (event_id, self.student_id, 'student', 'registered'))
        conn.commit()
        conn.close()
        messagebox.showinfo('Success', 'Successfully registered for the event!')

    def show_my_events(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # My events UI
        Label(self.content_frame,
              text="My Registered Events",
              font=self.style['title_font']).grid(row=0, column=0, sticky='w', pady=10)
        
        # Events list
        self.my_events_list = Listbox(self.content_frame,
                                    font=self.style['font'],
                                    width=70,
                                    height=20)
        self.my_events_list.grid(row=1, column=0, sticky='nsew', pady=10)
        
        # Configure grid weights
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Show loading while populating events
        def populate():
            self.populate_my_events()
            
        show_loading(self.content_frame, populate)

    def populate_my_events(self):
        self.my_events_list.delete(0, END)
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        c.execute("""SELECT e.id, e.event_name, e.event_time, e.event_venue, e.status 
                    FROM event e
                    JOIN attendance a ON e.id = a.event_id
                    WHERE a.user_id = ? AND a.user_type = 'student'
                    ORDER BY e.event_time""", (self.student_id,))
        events = c.fetchall()
        for event in events:
            status_color = {
                'Upcoming': 'blue',
                'Ongoing': 'green',
                'Completed': 'gray'
            }.get(event[4], 'black')
            
            self.my_events_list.insert('end', f"{event[1]} - {event[2]} - {event[3]} [{event[4]}]")
            self.my_events_list.itemconfig('end', fg=status_color)
        conn.close()

    def student_logout(self):
        self.right.destroy()
        admin_obj = Main(root)

class LoadingIndicator:
    def __init__(self, parent):
        self.parent = parent
        self.canvas = Canvas(parent, width=50, height=50, bg='white', highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self.angle = 0
        self.is_running = False
        
    def start(self):
        self.is_running = True
        self.canvas.place(relx=0.5, rely=0.5, anchor='center')
        self._animate()
        
    def stop(self):
        self.is_running = False
        self.canvas.place_forget()
        
    def _animate(self):
        if not self.is_running:
            return
            
        self.canvas.delete('all')
        # Draw loading circle
        x, y = 25, 25
        radius = 20
        start_angle = self.angle
        extent = 300
        
        self.canvas.create_arc(x-radius, y-radius, x+radius, y+radius,
                             start=start_angle, extent=extent,
                             width=3, style='arc')
        
        self.angle = (self.angle + 10) % 360
        self.parent.after(50, self._animate)

def show_loading(parent, operation):
    loading = LoadingIndicator(parent)
    loading.start()
    
    def run_operation():
        try:
            result = operation()
            parent.after(0, lambda: loading.stop())
            return result
        except Exception as e:
            parent.after(0, lambda: loading.stop())
            raise e
    
    thread = threading.Thread(target=run_operation)
    thread.start()
    return thread

home_obj = Home(root)
root.mainloop()