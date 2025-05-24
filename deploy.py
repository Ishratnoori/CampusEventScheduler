import PyInstaller.__main__
import os
import shutil
import sqlite3

def create_executable():
    # Ensure the assets directory exists
    if not os.path.exists('assets'):
        os.makedirs('assets')
        print("Created assets directory")

    # PyInstaller configuration
    PyInstaller.__main__.run([
        'main.py',  # Your main script
        '--name=CampusEventScheduler',  # Name of the executable
        '--onefile',  # Create a single executable file
        '--windowed',  # Don't show console window
        '--icon=assets/logo.ico',  # Application icon
        '--add-data=assets;assets',  # Include assets directory
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace existing build
    ])

    # Create a deployment directory
    if os.path.exists('deployment'):
        shutil.rmtree('deployment')
    os.makedirs('deployment')

    # Copy the executable to deployment directory
    shutil.copy('dist/CampusEventScheduler.exe', 'deployment/')
    
    # Copy assets directory to deployment
    shutil.copytree('assets', 'deployment/assets')

    # Initialize database in deployment directory
    db_path = os.path.join('deployment', 'college_events.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create tables
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

    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  event_id INTEGER,
                  user_id INTEGER,
                  user_type TEXT,
                  status TEXT,
                  attended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (event_id) REFERENCES event(id))''')

    # Create default admin account
    c.execute("""INSERT INTO admins 
                (username, password, email, full_name, role)
                VALUES (?, ?, ?, ?, ?)""",
             ('admin', 'admin123', 'admin@college.edu', 'System Administrator', 'super_admin'))

    conn.commit()
    conn.close()

    print("\nDeployment completed successfully!")
    print("You can find the executable in the 'deployment' directory")
    print("To run the application, double-click 'CampusEventScheduler.exe'")
    print("\nDefault admin credentials:")
    print("Username: admin")
    print("Password: admin123")

if __name__ == '__main__':
    create_executable() 