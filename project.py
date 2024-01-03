from tkinter import Tk,Frame,Label,Entry,Button,messagebox
from PIL import Image,ImageTk

fonts = ('Courier New', 13, 'bold')
fonts1 = ('Courier New', 17, 'bold')
admin = 'ADMIN'
password = 'PASSWORD'
student = 'STUDENT'
password1 = 'PASSWORD1'

root = Tk()

class Home:
    def __init__(self,root):
        self.root=root
        self.root.title("HOME")
        self.page = Frame(self.root,width=600,height=400)
        self.page.place(x=0,y=0)
        
        self.image = Image.open('../assets/bg.png')
        self.image = self.image.resize((600,400))
        self.image = ImageTk.PhotoImage(self.image)
        self.image_label = Label(self.page,image=self.image)
        self.image_label.place(x=0,y=0)


        self.main_label = Label(self.page , text = 'WELCOME', font = fonts1)
        self.main_label.place(x=235,y=50)
        self.main_label2 = Label(self.page , text = "COLLEGE EVENTS" , font = fonts)
        self.main_label2.place(x=217,y=110)
        self.main_label_btn = Button(self.page,text='ENTER',font=fonts1,command=self.home_login)
        self.main_label_btn.place(x=240,y=200)


    def home_login(self):    
        self.page.destroy()
        home_obj = Main(root)



class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("LOGIN PAGE")
        self.right =Frame(self.root,width = 600, height = 400,bg='darkseagreen1')
        self.right.place(x = 0, y = 0 )
        
        self.admin_logo = Image.open('../assets/administrator.png')
        
        self.admin_logo = self.admin_logo.resize((100, 100))

        self.admin_logo = ImageTk.PhotoImage(self.admin_logo)

        self.admin_logo_logo_lbl = Label(self.right, image = self.admin_logo)
        self.admin_logo_logo_lbl.place(x = 50, y= 30)
       
        self.admin__login = Label(self.right,text="Admin login")
        self.admin__login.place(x=100,y=125) 
        self.admin_name = Label(self.right, text = 'USER ID', bg = 'steel blue', fg ='white', font = fonts,width = 9)
        self.admin_name.place(x = 50, y = 170)
        self.admin_name_entry = Entry(self.right, width = 10, font = fonts)
        self.admin_name_entry.place(x = 150, y = 170)
        self.admin_pass = Label(self.right, text = 'PASSWORD', bg = 'steel blue', fg ='white', font = fonts, width = 9)
        self.admin_pass.place(x = 50, y = 200)
        self.admin_pass_entry = Entry(self.right, width = 10, font = fonts)
        self.admin_pass_entry.place(x = 150, y = 200)

        self.admin_login_btn = Button(self.right, text = 'LOGIN', font = fonts, command = self.admin_login)
        self.admin_login_btn.place(x = 100, y = 250)


        self.left =Frame(self.root, width = 600, height = 400,bg='darkseagreen1')
        self.left.place(x = 250, y = 0 )


        self.student_name = Label(self.left, text = 'USER ID', bg = 'steel blue', fg ='white', font = fonts,width=9)
        self.student_name.place(x = 50, y = 170)
        self.student_name_entry = Entry(self.left, width = 10, font = fonts)
        self.student_name_entry.place(x = 150, y = 170)
        
        self.student_logo = Image.open('../assets/student.png')
        
        self.student_logo = self.student_logo.resize((100, 100))

        self.student_logo = ImageTk.PhotoImage(self.student_logo)

        self.student_logo_lbl = Label(self.left, image = self.student_logo)
        self.student_logo_lbl.place(x = 100, y= 30)

        self.student__login = Label(self.left,text="Student login")
        self.student__login.place(x=100,y=125)

        self.student_pass = Label(self.left, text = 'PASSWORD', bg = 'steel blue', fg ='white', font = fonts, width = 9)
        self.student_pass.place(x = 50, y = 200)
        self.student_pass_entry = Entry(self.left, width = 10, font = fonts)
        self.student_pass_entry.place(x = 150, y = 200)

        self.student_login_btn = Button(self.left, text = 'LOGIN', font = fonts,command = self.student_login)
        self.student_login_btn.place(x = 100, y = 250)
    

    def admin_login(self):
        global admin, password
        self.a_name = self.admin_name_entry.get()
        self.a_pass = self.admin_pass_entry.get()
        if self.a_name == admin:
            if self.a_pass == password:
                self.right.destroy()
                self.left.destroy()
                admin_obj = Admin(root)
            else:
                messagebox.showerror('INVALID','INCORRECT PASSWORD')
        else:
                messagebox.showerror('INVALID','USER ID INVALID')



    def student_login(self):
        global student, password1
        self.b_name = self.student_name_entry.get()
        self.b_pass = self.student_pass_entry.get()
        if self.b_name == student:
            if self.b_pass == password1:
                self.right.destroy()
                self.left.destroy()
                student_obj = Student(root)
            else:
                messagebox.showerror('INVALID','INCORRECT PASSWORD')
        else:
                messagebox.showerror('INVALID','USER ID INVALID')
      

class Admin:
    def __init__(self, root):
        self.root = root
        self.root.title("ADMIN DASHBOARD")
        self.right = Frame(self.root, width = 600, height = 400)
        self.right.place(x = 0, y = 0)

        self.student__login = Label(self.right,text="EVENT LIST",bg='White',fg='Black')
        self.student__login.place(x=170,y=10)


class Student:
    def __init__(self, root):
        self.root = root
        self.root.title('STUDENT DASHBOARD')
        self.left = Frame(self.root, width = 600, height = 400)
        self.left.place(x = 0, y = 0)

        self.student__login = Label(self.left,text="HELLO PARTICIPANTS!",fg='red',font=fonts1)
        self.student__login.place(x=200,y=40)

        self.regno_name = Label(self.left, text = 'PARTICIPANT LIST',fg ='black', font = fonts)
        self.regno_name.place(x = 100, y = 140)
        self.regno_name_entry = Entry(self.left,width=20, font = fonts)
        self.regno_name_entry.place(x = 300, y = 140)

root.geometry('600x400+550+200')
home = Home(root)
root.mainloop()