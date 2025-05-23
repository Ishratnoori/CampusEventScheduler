from tkinter import Tk, Frame, Label, Entry, Button, Listbox, Scrollbar, messagebox, Toplevel, END, ANCHOR, Text, StringVar, LabelFrame, Radiobutton, Canvas, Checkbutton, filedialog, BooleanVar
from PIL import Image, ImageTk
import sqlite3
import tkinter.ttk as ttk
from tkinter.ttk import Separator
import threading
import time
import re  # Add this at the top with other imports
import json
import os
import shutil

fonts = ('Courier New', 13, 'bold')
fonts1 = ('Courier New', 17, 'bold')

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

# Remove the Home class and start directly with Main class
root = Tk()
root.iconbitmap(default="assets/logo.ico")
root.title("CAMPUS EVENT SCHEDULER")
root.geometry('800x600+50+50')

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("CAMPUS EVENT SCHEDULER")
        
        # Set window size
        self.root.geometry('800x600')
        
        # Modern styling
        self.style = {
            'bg': 'white',
            'fg': '#212529',
            'button_bg': '#0d6efd',
            'button_fg': 'white',
            'button_hover': '#0b5ed7',
            'font': ('Segoe UI', 11),
            'title_font': ('Segoe UI', 24, 'bold'),
            'subtitle_font': ('Segoe UI', 14),
            'card_bg': 'white',
            'border_color': '#dee2e6',
            'input_bg': 'white',
            'input_border': '#ced4da'
        }

        # Main container
        self.main_frame = Frame(self.root, bg='white')
        self.main_frame.pack(fill='both', expand=True)

        # Show welcome screen by default
        self.return_to_welcome()

    def return_to_welcome(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create welcome screen
        self.welcome_frame = Frame(self.main_frame, bg='#333333')
        self.welcome_frame.place(relwidth=1, relheight=1)

        # Load and set background image
        try:
            self.image = Image.open('assets/bg2.jpg')
            # Get the window size
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            # If window size is not yet available, use default size
            if window_width <= 1:
                window_width = 800
            if window_height <= 1:
                window_height = 600
                
            # Resize image to match window size
            self.image = self.image.resize((window_width, window_height), Image.Resampling.LANCZOS)
            self.image = ImageTk.PhotoImage(self.image)
            
            # Create background label that fills the entire frame
            self.image_label = Label(self.welcome_frame, image=self.image)
            self.image_label.place(relwidth=1, relheight=1)
            
            # Bind resize event to update background
            def resize_background(event):
                # Get new window size
                new_width = event.width
                new_height = event.height
                
                # Resize image to new dimensions
                resized_image = Image.open('assets/bg2.jpg')
                resized_image = resized_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.image = ImageTk.PhotoImage(resized_image)
                self.image_label.configure(image=self.image)
            
            # Bind the resize event
            self.welcome_frame.bind('<Configure>', resize_background)
            
        except Exception as e:
            print(f"Error loading background image: {e}")
            # Set a solid color background if image loading fails
            self.welcome_frame.configure(bg='#333333')

        # Welcome text with modern styling
        self.welcome_content = Frame(self.welcome_frame, bg='#333333')
        self.welcome_content.place(relx=0.5, rely=0.5, anchor='center', width=600, height=400)

        self.main_label = Label(self.welcome_content, 
                              text='WELCOME TO', 
                              font=('Helvetica', 40, 'bold'),
                              bg='#333333',
                              fg='white')
        self.main_label.place(relx=0.5, rely=0.3, anchor='center')

        self.main_label2 = Label(self.welcome_content,
                               text="CAMPUS EVENT SCHEDULER",
                               font=('Helvetica', 30, 'bold'),
                               bg='#333333',
                               fg='white')
        self.main_label2.place(relx=0.5, rely=0.45, anchor='center')

        # Description
        self.description = Label(self.welcome_content,
                               text="Your one-stop solution for managing and participating in campus events",
                               font=('Helvetica', 14),
                               bg='#333333',
                               fg='white',
                               wraplength=500)
        self.description.place(relx=0.5, rely=0.6, anchor='center')

        # Enter button with hover effect
        self.main_label_btn = Button(self.welcome_content,
                                   text='ENTER',
                                   font=('Helvetica', 20, 'bold'),
                                   bg='#4a90e2',
                                   fg='white',
                                   command=self.show_login_screen,
                                   width=15,
                                   cursor='hand2')
        self.main_label_btn.place(relx=0.5, rely=0.8, anchor='center')

        # Add hover effect
        def on_enter(e):
            self.main_label_btn['bg'] = '#357abd'

        def on_leave(e):
            self.main_label_btn['bg'] = '#4a90e2'

        self.main_label_btn.bind("<Enter>", on_enter)
        self.main_label_btn.bind("<Leave>", on_leave)

    def show_login_screen(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Content container
        self.content_frame = Frame(self.main_frame, bg='white')
        self.content_frame.pack(fill='both', expand=True)

        # Title
        title_frame = Frame(self.content_frame, bg='white', pady=30)
        title_frame.pack(fill='x')
        
        Label(title_frame,
              text="CAMPUS EVENT SCHEDULER",
              font=self.style['title_font'],
              fg='black',
              bg='white').pack()

        # Login container
        login_frame = Frame(self.content_frame, bg='white')
        login_frame.pack(expand=True)

        # Admin section
        admin_frame = Frame(login_frame, 
                          bg='white',
                          highlightbackground=self.style['border_color'],
                          highlightthickness=1,
                          padx=30,
                          pady=30)
        admin_frame.grid(row=0, column=0, padx=20)

        # Admin logo
        self.admin_logo = Image.open('assets/administrator.png')
        self.admin_logo = self.admin_logo.resize((150, 150))
        self.admin_logo = ImageTk.PhotoImage(self.admin_logo)
        admin_logo_lbl = Label(admin_frame, image=self.admin_logo, bg='white')
        admin_logo_lbl.pack(pady=(0, 20))

        Label(admin_frame,
              text="Admin Login",
              font=self.style['subtitle_font'],
              bg='white',
              fg=self.style['fg']).pack(pady=(0, 20))

        # Admin login fields
        admin_fields = Frame(admin_frame, bg='white')
        admin_fields.pack(fill='x', pady=10)

        Label(admin_fields,
              text='Username',
              font=self.style['font'],
              bg='white',
              fg=self.style['fg']).pack(anchor='w')
        
        self.admin_name_entry = Entry(admin_fields,
                                    font=self.style['font'],
                                    bg=self.style['input_bg'],
                                    relief='solid',
                                    borderwidth=1)
        self.admin_name_entry.pack(fill='x', pady=(5, 15))

        Label(admin_fields,
              text='Password',
              font=self.style['font'],
              bg='white',
              fg=self.style['fg']).pack(anchor='w')
        
        self.admin_pass_entry = Entry(admin_fields,
                                    font=self.style['font'],
                                    show='*',
                                    bg=self.style['input_bg'],
                                    relief='solid',
                                    borderwidth=1)
        self.admin_pass_entry.pack(fill='x', pady=(5, 15))

        # Admin buttons
        admin_buttons = Frame(admin_frame, bg='white')
        admin_buttons.pack(fill='x', pady=10)

        Button(admin_buttons,
               text='LOGIN',
               font=self.style['font'],
               bg=self.style['button_bg'],
               fg='white',
               relief='flat',
               padx=30,
               pady=10,
               command=self.admin_login,
               cursor='hand2').pack(side='right', pady=5)

        # Student section
        student_frame = Frame(login_frame,
                            bg='white',
                            highlightbackground=self.style['border_color'],
                            highlightthickness=1,
                            padx=30,
                            pady=30)
        student_frame.grid(row=0, column=1, padx=20)

        # Student logo
        self.student_logo = Image.open('assets/student.png')
        self.student_logo = self.student_logo.resize((150, 150))
        self.student_logo = ImageTk.PhotoImage(self.student_logo)
        student_logo_lbl = Label(student_frame, image=self.student_logo, bg='white')
        student_logo_lbl.pack(pady=(0, 20))

        Label(student_frame,
              text="Student Login",
              font=self.style['subtitle_font'],
              bg='white',
              fg=self.style['fg']).pack(pady=(0, 20))

        # Student login fields
        student_fields = Frame(student_frame, bg='white')
        student_fields.pack(fill='x', pady=10)

        Label(student_fields,
              text='Username',
              font=self.style['font'],
              bg='white',
              fg=self.style['fg']).pack(anchor='w')
        
        self.student_name_entry = Entry(student_fields,
                                      font=self.style['font'],
                                      bg=self.style['input_bg'],
                                      relief='solid',
                                      borderwidth=1)
        self.student_name_entry.pack(fill='x', pady=(5, 15))

        Label(student_fields,
              text='Password',
              font=self.style['font'],
              bg='white',
              fg=self.style['fg']).pack(anchor='w')
        
        self.student_pass_entry = Entry(student_fields,
                                      font=self.style['font'],
                                      show='*',
                                      bg=self.style['input_bg'],
                                      relief='solid',
                                      borderwidth=1)
        self.student_pass_entry.pack(fill='x', pady=(5, 15))

        # Student buttons
        student_buttons = Frame(student_frame, bg='white')
        student_buttons.pack(fill='x', pady=10)

        Button(student_buttons,
               text='LOGIN',
               font=self.style['font'],
               bg=self.style['button_bg'],
               fg='white',
               relief='flat',
               padx=30,
               pady=10,
               command=self.student_login,
               cursor='hand2').pack(side='left', padx=10, pady=5)

        Button(student_buttons,
               text='SIGN UP',
               font=self.style['font'],
               bg=self.style['button_bg'],
               fg='white',
               relief='flat',
               padx=30,
               pady=10,
               command=self.student_signup,
               cursor='hand2').pack(side='right', pady=5)

        # Back button
        Button(self.content_frame,
               text='BACK',
               font=self.style['font'],
               bg=self.style['button_bg'],
               fg='white',
               relief='flat',
               padx=30,
               pady=10,
               command=self.return_to_welcome,
               cursor='hand2').pack(side='bottom', pady=20)

        # Add hover effects
        for btn in [b for b in self.content_frame.winfo_children() if isinstance(b, Button)]:
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.style['button_hover']))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.style['button_bg']))

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
            self.main_frame.destroy()
            admin_obj = Admin(root, admin_data[0])  # Pass admin ID
        else:
            messagebox.showerror('ERROR', 'Invalid username or password')
        conn.close()

    def student_login(self):
        username = self.student_name_entry.get().strip()
        password = self.student_pass_entry.get()
        
        if not username or not password:
            messagebox.showerror('ERROR', 'Please fill in all fields')
            return
            
        conn = sqlite3.connect('college_events.db')
        c = conn.cursor()
        
        try:
            c.execute("SELECT * FROM students WHERE username = ? AND password = ?", (username, password))
            student_data = c.fetchone()
            
            if student_data:
                messagebox.showinfo('SUCCESS', f'Welcome, {student_data[4]}!')
                self.main_frame.destroy()
                student_obj = Student(root, student_data[0])  # Pass student ID
            else:
                messagebox.showerror('ERROR', 'Invalid username or password')
        except Exception as e:
            messagebox.showerror('ERROR', f'Login failed: {str(e)}')
        finally:
            conn.close()

    def student_signup(self):
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Form container with card-like appearance
        form_frame = Frame(self.main_frame,
                         bg='white',
                         highlightbackground='#e1e4e8',
                         highlightthickness=1,
                         padx=40,
                         pady=30)
        form_frame.pack(fill='both', expand=True)

        # Title with modern styling
        title_frame = Frame(form_frame, bg='white')
        title_frame.pack(fill='x', pady=(0, 30))

        Label(title_frame,
              text="Student Registration",
              font=('Segoe UI', 24, 'bold'),
              bg='white',
              fg='#1a1a1a').pack()

        Label(title_frame,
              text="Create your student account",
              font=('Segoe UI', 12),
              bg='white',
              fg='#666666').pack(pady=(5, 0))

        # Back button
        back_btn = Button(title_frame,
                         text='← Back',
                         font=('Segoe UI', 11),
                         bg='white',
                         fg='#0d6efd',
                         relief='flat',
                         command=self.show_login_screen,
                         cursor='hand2')
        back_btn.pack(side='left', pady=(0, 20))

        # Validation message labels
        validation_labels = {}

        def validate_field(event, field, value):
            label = validation_labels[field]
            if not value.strip():
                label.config(text=f"{field.replace('_', ' ').title()} is required", fg='#dc3545')
                return False

            if field == 'username':
                if not validate_username(value):
                    label.config(text="Username must be 4-20 characters, letters, numbers, and underscores only", fg='#dc3545')
                    return False
                label.config(text="✓ Username is valid", fg='#28a745')

            elif field == 'password':
                is_valid, msg = validate_password(value)
                if not is_valid:
                    label.config(text=msg, fg='#dc3545')
                    return False
                label.config(text="✓ Password is valid", fg='#28a745')

            elif field == 'email':
                if not validate_email(value):
                    label.config(text="Please enter a valid email address", fg='#dc3545')
                    return False
                label.config(text="✓ Email is valid", fg='#28a745')

            elif field == 'student_id':
                if not validate_student_id(value):
                    label.config(text="Student ID must be 2 letters followed by 8 numbers (e.g., CS12345678)", fg='#dc3545')
                    return False
                label.config(text="✓ Student ID is valid", fg='#28a745')

            elif field == 'department':
                if len(value.strip()) < 2:
                    label.config(text="Department name is too short", fg='#dc3545')
                    return False
                label.config(text="✓ Department is valid", fg='#28a745')

            elif field == 'full_name':
                if len(value.strip()) < 3:
                    label.config(text="Full name is too short", fg='#dc3545')
                    return False
                label.config(text="✓ Full name is valid", fg='#28a745')

            return True

        # Create two columns for fields
        fields_frame = Frame(form_frame, bg='white')
        fields_frame.pack(fill='both', expand=True)

        left_frame = Frame(fields_frame, bg='white')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        right_frame = Frame(fields_frame, bg='white')
        right_frame.pack(side='right', fill='both', expand=True, padx=(15, 0))

        # Form fields with validation
        fields = [
            ('Username:', 'username', '4-20 characters, letters, numbers, and underscores only'),
            ('Password:', 'password', 'Min 8 characters, 1 uppercase, 1 lowercase, 1 number'),
            ('Email:', 'email', 'Valid email address'),
            ('Full Name:', 'full_name', 'Your full name'),
            ('Student ID:', 'student_id', 'Format: 2 letters followed by 8 numbers (e.g., CS12345678)'),
            ('Department:', 'department', 'Your department (e.g., Computer Science)')
        ]

        entries = {}
        for i, (label_text, field, hint) in enumerate(fields):
            # Choose frame based on index
            parent_frame = left_frame if i < 3 else right_frame
            
            # Field container
            field_frame = Frame(parent_frame, bg='white')
            field_frame.pack(fill='x', pady=(0, 20))

            # Label
            Label(field_frame,
                  text=label_text,
                  font=('Segoe UI', 11, 'bold'),
                  bg='white',
                  fg='#1a1a1a').pack(anchor='w')

            # Entry
            if field == 'password':
                entry = Entry(field_frame,
                            width=30,
                            font=('Segoe UI', 11),
                            show='*',
                            bg='#f8f9fa',
                            relief='solid',
                            borderwidth=1)
            else:
                entry = Entry(field_frame,
                            width=30,
                            font=('Segoe UI', 11),
                            bg='#f8f9fa',
                            relief='solid',
                            borderwidth=1)

            entry.pack(fill='x', pady=(5, 5))
            entries[field] = entry

            # Hint label
            Label(field_frame,
                  text=hint,
                  font=('Segoe UI', 9),
                  bg='white',
                  fg='#666666').pack(anchor='w')

            # Validation label
            validation_label = Label(field_frame,
                                   text="",
                                   font=('Segoe UI', 9),
                                   bg='white',
                                   fg='#666666')
            validation_label.pack(anchor='w', pady=(2, 0))
            validation_labels[field] = validation_label

            # Bind validation to entry
            entry.bind('<KeyRelease>', lambda e, f=field: validate_field(e, f, entries[f].get()))

        # Button container
        button_frame = Frame(form_frame, bg='white')
        button_frame.pack(fill='x', pady=(20, 0))

        def register():
            # Validate all fields
            all_valid = True
            for field, entry in entries.items():
                if not validate_field(None, field, entry.get()):
                    all_valid = False

            if not all_valid:
                messagebox.showerror('Error', 'Please fix the validation errors before proceeding')
                return

            # Get values
            values = {field: entry.get().strip() for field, entry in entries.items()}

            # Check if username, email, or student ID already exists
            conn = sqlite3.connect('college_events.db')
            c = conn.cursor()
            
            try:
                c.execute("SELECT * FROM students WHERE username = ? OR email = ? OR student_id = ?",
                         (values['username'], values['email'], values['student_id']))
                if c.fetchone():
                    messagebox.showerror('Error', 'Username, email, or student ID already exists')
                    return
                
                # Insert new student
                c.execute("""INSERT INTO students 
                            (username, password, email, full_name, student_id, department)
                            VALUES (?, ?, ?, ?, ?, ?)""",
                         (values['username'], values['password'], values['email'],
                          values['full_name'], values['student_id'], values['department']))
                
                conn.commit()
                messagebox.showinfo('Success', 'Registration successful! Please login.')
                self.show_login_screen()  # Go back to login screen
            except Exception as e:
                messagebox.showerror('Error', f'Registration failed: {str(e)}')
            finally:
                conn.close()

        # Register button with modern styling
        register_btn = Button(button_frame,
                            text='REGISTER',
                            font=('Segoe UI', 12, 'bold'),
                            bg='#0d6efd',
                            fg='white',
                            relief='flat',
                            padx=40,
                            pady=10,
                            command=register,
                            cursor='hand2')
        register_btn.pack(anchor='center')

        # Add hover effect
        def on_enter(e):
            register_btn['bg'] = '#0b5ed7'
        
        def on_leave(e):
            register_btn['bg'] = '#0d6efd'
        
        register_btn.bind("<Enter>", on_enter)
        register_btn.bind("<Leave>", on_leave)


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
            'bg': '#f8f9fa',  # Light gray background
            'fg': '#212529',  # Dark gray text
            'button_bg': '#0d6efd',  # Primary blue
            'button_fg': 'white',
            'button_hover': '#0b5ed7',  # Darker blue for hover
            'danger_bg': '#dc3545',  # Red for logout
            'danger_hover': '#bb2d3b',  # Darker red for hover
            'font': ('Segoe UI', 11),  # Modern system font
            'title_font': ('Segoe UI', 20, 'bold'),
            'header_bg': '#0d6efd',  # Blue header
            'card_bg': 'white',  # White for cards
            'border_color': '#dee2e6'  # Light gray for borders
        }

        # Main container with shadow effect
        self.main_container = Frame(self.right, bg=self.style['bg'], padx=20, pady=20)
        self.main_container.grid(row=0, column=0, sticky='nsew')
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        # Header with gradient effect
        self.header = Frame(self.main_container, bg=self.style['header_bg'], height=70)
        self.header.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
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
                               bg=self.style['header_bg'],
                               fg='white')
        self.title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Update title after loading
        def update_title():
            admin_name = get_admin_name()
            self.title_label.config(text=f"Welcome, {admin_name}")
            
        self.root.after(100, update_title)

        # Navigation buttons with modern styling
        self.nav_frame = Frame(self.main_container, bg=self.style['bg'])
        self.nav_frame.grid(row=1, column=0, sticky='ns', padx=(0, 20))

        self.buttons = [
            ("Events", self.show_events)
        ]

        for i, (text, command) in enumerate(self.buttons):
            btn = Button(self.nav_frame, 
                        text=text,
                        font=self.style['font'],
                        bg=self.style['button_bg'],
                        fg='white',
                        command=command,
                        width=15,
                        cursor='hand2',
                        relief='flat',
                        padx=20,
                        pady=10)
            btn.grid(row=i, column=0, pady=5, sticky='ew')
            
            # Add hover effect
            def on_enter(e, btn=btn):
                btn['bg'] = self.style['button_hover']
            
            def on_leave(e, btn=btn):
                btn['bg'] = self.style['button_bg']
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        # Main content area with card-like appearance
        self.content_frame = Frame(self.main_container, 
                                 bg=self.style['card_bg'],
                                 highlightbackground=self.style['border_color'],
                                 highlightthickness=1)
        self.content_frame.grid(row=1, column=1, sticky='nsew', padx=20, pady=20)

        # Show events by default
        self.show_events()

        # Logout button with modern styling
        self.logout_btn = Button(self.main_container,
                               text='LOGOUT',
                               font=self.style['font'],
                               bg=self.style['danger_bg'],
                               fg='white',
                               command=self.admin_logout,
                               cursor='hand2',
                               relief='flat',
                               padx=20,
                               pady=10)
        self.logout_btn.grid(row=0, column=1, sticky='e', padx=20, pady=10)
        
        # Add hover effect for logout button
        def on_enter(e):
            self.logout_btn['bg'] = self.style['danger_hover']
        
        def on_leave(e):
            self.logout_btn['bg'] = self.style['danger_bg']
        
        self.logout_btn.bind("<Enter>", on_enter)
        self.logout_btn.bind("<Leave>", on_leave)

    def show_events(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Add event button with modern styling
        add_btn = Button(self.content_frame,
                        text='Add New Event',
                        font=self.style['font'],
                        bg=self.style['button_bg'],
                        fg='white',
                        command=self.add_event_window,
                        cursor='hand2',
                        relief='flat',
                        padx=20,
                        pady=10)
        add_btn.grid(row=0, column=0, sticky='w', pady=10)
        
        # Add hover effect
        def on_enter(e):
            add_btn['bg'] = self.style['button_hover']
        
        def on_leave(e):
            add_btn['bg'] = self.style['button_bg']
        
        add_btn.bind("<Enter>", on_enter)
        add_btn.bind("<Leave>", on_leave)

        # Event list with modern styling
        list_frame = Frame(self.content_frame, bg=self.style['card_bg'])
        list_frame.grid(row=1, column=0, sticky='nsew', pady=10)
        
        self.event_list = Listbox(list_frame,
                                 font=self.style['font'],
                                 width=70,
                                 height=20,
                                 bg='white',
                                 fg=self.style['fg'],
                                 selectbackground=self.style['button_bg'],
                                 selectforeground='white',
                                 relief='flat',
                                 highlightthickness=1,
                                 highlightbackground=self.style['border_color'])
        self.event_list.pack(side='left', fill='both', expand=True)

        scrollbar = Scrollbar(list_frame,
                            orient="vertical",
                            command=self.event_list.yview)
        scrollbar.pack(side='right', fill='y')

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
        # Create a new window for each event addition
        add_window = Toplevel(self.root)
        add_window.title('Add Event')
        add_window.geometry('600x700')
        add_window.configure(bg=self.style['bg'])
        add_window.grab_set()

        # Form container with card-like appearance
        form_frame = Frame(add_window, 
                         bg=self.style['card_bg'],
                         highlightbackground=self.style['border_color'],
                         highlightthickness=1,
                         padx=30,
                         pady=30)
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Form fields
        fields = [
            ('Event Name:', 'event_name'),
            ('Event Time:', 'event_time'),
            ('Event Venue:', 'event_venue'),
            ('Description:', 'description'),
            ('Requirements:', 'requirements')
        ]

        entries = {}
        for i, (label, field) in enumerate(fields):
            Label(form_frame,
                  text=label,
                  font=self.style['font'],
                  bg=self.style['card_bg'],
                  fg=self.style['fg']).grid(row=i, column=0, padx=10, pady=10, sticky='w')
            
            if field in ['description', 'requirements']:
                # Text areas for longer content
                entries[field] = Text(form_frame,
                                   height=4,
                                   width=40,
                                   font=self.style['font'],
                                   relief='solid',
                                   borderwidth=1)
            else:
                # Regular entry fields
                entries[field] = Entry(form_frame,
                                    width=40,
                                    font=self.style['font'],
                                    relief='solid',
                                    borderwidth=1)

            entries[field].grid(row=i, column=1, padx=10, pady=10, sticky='ew')

        def add_event():
            # Get values from entries
            values = {field: entry.get() if not isinstance(entry, Text) else entry.get('1.0', 'end-1c')
                     for field, entry in entries.items()}

            if all(values.values()):
                conn = sqlite3.connect('college_events.db')
                c = conn.cursor()
                
                # Insert event with default status 'Upcoming'
                c.execute("""INSERT INTO event 
                            (event_name, event_time, event_venue, description, requirements, status, created_by)
                            VALUES (?, ?, ?, ?, ?, ?, ?)""",
                         (values['event_name'], values['event_time'], values['event_venue'],
                          values['description'], values['requirements'], 'Upcoming', self.admin_id))
                
                event_id = c.lastrowid
                
                # Add to event history
                c.execute("""INSERT INTO event_history 
                            (event_id, action, changed_by)
                            VALUES (?, ?, ?)""",
                         (event_id, 'Created', self.admin_id))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo('Success', 'Event added successfully.')
                add_window.destroy()
                self.show_events()
            else:
                messagebox.showerror('Error', 'Please fill in all fields.')

        # Add event button with modern styling
        Button(form_frame,
               text='Add Event',
               font=self.style['font'],
               bg=self.style['button_bg'],
               fg='white',
               command=add_event,
               cursor='hand2',
               relief='flat',
               padx=30,
               pady=10).grid(row=len(fields), column=0, columnspan=2, pady=20)

    def add_event(self):
        self.add_event_window()

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
        self.animate()
        
    def stop(self):
        self.is_running = False
        self.canvas.place_forget()
        
    def animate(self):
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
        self.parent.after(50, self.animate)

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

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    # At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def validate_student_id(student_id):
    # Assuming student ID format: 2 letters followed by 8 numbers
    pattern = r'^[A-Z]{2}\d{8}$'
    return re.match(pattern, student_id) is not None

def validate_username(username):
    # Username should be 4-20 characters, alphanumeric with underscores
    pattern = r'^[a-zA-Z0-9_]{4,20}$'
    return re.match(pattern, username) is not None

main_obj = Main(root)
root.mainloop()