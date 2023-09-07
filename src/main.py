import sqlite3
import datetime
import bcrypt
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmg
from tkinter.scrolledtext import *
from PIL import ImageTk

root = Tk()
root.title("The Progress Book")
root.geometry("1280x700+0+0")
root.resizable(False,False)
style = ttk.Style()
style.theme_use("default")

bg=ImageTk.PhotoImage(file="images/bgimage.png")
bg2=ImageTk.PhotoImage(file="images/bgimage2.png")
bg3=ImageTk.PhotoImage(file="images/bgimage3.png")
bg4=ImageTk.PhotoImage(file="images/bgimage4.png")
bg5=ImageTk.PhotoImage(file="images/bgimage5.png")
bg6=ImageTk.PhotoImage(file="images/bgimage6.png")
bg7=ImageTk.PhotoImage(file="images/bgimage7.png")
bg8=ImageTk.PhotoImage(file="images/bgimage8.png")
bg9=ImageTk.PhotoImage(file="images/bgimage9.png")
bg10=ImageTk.PhotoImage(file="images/bgimage10.png")
bgimagehome=ImageTk.PhotoImage(file="images/bgimagehome.png")
bgtop1=ImageTk.PhotoImage(file="images/top1.png")
bgtop2=ImageTk.PhotoImage(file="images/top2.png")
bgtop3=ImageTk.PhotoImage(file="images/top3.png")
bgtop4=ImageTk.PhotoImage(file="images/top4.png")

jt,mt,st = 0,0,0
curr_date = str(datetime.datetime.now().replace(second=0, microsecond=0))

conn = sqlite3.connect('detail.db')
c = conn.cursor()

correctDate = None
def check_date(year,month,date):
    try:
        newDate = datetime.datetime(year, month, date)
        correctDate = True
    except ValueError:
        correctDate = False
    return (str(correctDate))

def create():
    c.execute("""CREATE TABLE IF NOT EXISTS USER (
                USER_ID VARCHAR(20) PRIMARY KEY NOT NULL,
                USER_TYPE VARCHAR(20) NOT NULL,
                PASSWORD VARCHAR(255) NOT NULL,
                ENTRY_DATE INTEGER,
                JT  INTEGER,
                MT  INTEGER,
                ST  INTEGER
                );""")
    curr_date = str(datetime.datetime.now().replace(second=0, microsecond=0))
    salt = bcrypt.gensalt()
    check = c.execute("SELECT * FROM USER WHERE USER_TYPE = 'ADMIN'")
    no_of_users = len(c.fetchall())
    if(no_of_users==0):
        c.execute("INSERT INTO USER (USER_ID, USER_TYPE, PASSWORD, ENTRY_DATE, JT, MT, ST) VALUES (:name, :type, :password, :dt, :jt, :mt, :st)",{'name': 'admin', 'type': 'ADMIN', 'password': bcrypt.hashpw(b'admin', salt), 'dt': curr_date, 'jt': 0, 'mt': 0, 'st': 0})
        conn.commit()

create()

def login():
    def Forget_Password():
        tmg.showinfo("Forget Password", "Please Contact System Admin !", parent=root)

    def login_func():
        name = usernameS.get()
        password = passwordS.get()
        if(name =="" or password ==""):
            tmg.showwarning("Error", "All fields are required !", parent=root)
        elif(len(name)>0):
            c.execute("SELECT * FROM USER WHERE USER_ID = :name", {'name': name})
            data = c.fetchall()
            if not data:
                tmg.showwarning("Error", "Incorrect Username/Password entered !", parent=root)
            elif(name == data[0][0] and bcrypt.checkpw(password.encode(),data[0][2])):
                tmg.showinfo("Welcome", "Welcome to the system !", parent=root)
                c.execute("UPDATE USER set ENTRY_DATE = :date WHERE USER_ID = :name", {'date': curr_date,'name': name})
                conn.commit()
                home(data[0][:2])
                Frame_login.destroy()
                login_button.destroy()
            else:
                tmg.showwarning("Error","Incorrect Username/Password entered !", parent=root)

    global bg_image
    bg_image = Label(root, image=bg)
    bg_image.place(x=0, y=0, relwidth=1, relheight=1)

    Frame_login = Frame(root,bg="white")
    Frame_login.place(x=150,y=150,height=340,width=500)

    title= Label(Frame_login,text="Login Here",font=("Impact",35,"bold"),fg="#d77337",bg="white")
    title.place(x=90,y=30)

    usernameS = StringVar()
    passwordS = StringVar()

    label_user = Label(Frame_login, text="Username", font=("Goudy old style", 15, "bold"), fg="grey", bg="white")
    label_user.place(x=90, y=100)
    usernamename_entry = Entry(Frame_login, textvariable=usernameS,font=("times new roman",15),bg="light grey")
    usernamename_entry.place(x=90, y=130, width = 350, height = 35)

    label_password = Label(Frame_login, text="Password", font=("Goudy old style", 15, "bold"), fg="grey", bg="white")
    label_password.place(x=90, y=180)
    password_entry = Entry(Frame_login, show="*",textvariable=passwordS,font=("times new roman",15),bg="light grey")
    password_entry.place(x=90, y=210, width = 350, height = 35)

    forget_button=Button(Frame_login,text="Forget Password ?",command=Forget_Password, bg="white", fg="#d77337",bd=0,font=("times new roman",12))
    forget_button.place(x=90, y=280)
    login_button = Button(root,command=login_func, text="Login", fg="white", bg="#d77337", font=("times new roman", 20))
    login_button.place(x=300, y=470,height=40,width=180)


def home(user_data):

    def admin_portal():

        def add_user():
            def add():
                name = add_useridE.get()
                password = add_passwordE.get()
                salt = bcrypt.gensalt()
                test = bcrypt.hashpw(password.encode(), salt)
                type = add_user_type.get()
                if(name =="" or password =="" or add_repasswordE.get()==""):
                    tmg.showwarning("Error", "All fields are required !", parent=add_user_top)
                elif(password!=add_repasswordE.get()):
                    tmg.showwarning("Error", "Please check Password and Re-Password !", parent=add_user_top)
                elif(type=="NULL"):
                    tmg.showwarning("Error","Please Select User type !", parent=add_user_top)
                else:
                    value= tmg.askquestion("Add","Do you want to add "+name+" as "+type+"?")
                    if(value=='yes'):
                        curr_date = str(datetime.datetime.now().replace(second=0, microsecond=0))
                        c.execute("INSERT INTO USER(USER_ID, USER_TYPE, PASSWORD, ENTRY_DATE, JT, MT, ST) VALUES (:name, :type, :password, :date, :jt, :mt, :st)", {'name': name, 'type': type, 'password': test, 'date': curr_date, 'jt': 0, 'mt': 0, 'st': 0})
                        conn.commit()
                        global count
                        table_admin.insert(parent='', index='end', iid=count, text=(count + 1),values=(add_useridE.get(), add_user_type.get(), curr_date))
                        count += 1
                        add_useridE.delete(0, END)
                        add_repasswordE.delete(0, END)
                        add_passwordE.delete(0, END)
                        add_user_top.destroy()

            add_user_top= Toplevel(Frame_right,bg="white")
            add_user_top.title("Add User")
            add_user_top.geometry("600x300+0+0")
            add_user_top.resizable(False,False)
            TOP_BG = Label(add_user_top, image=bgtop1)
            TOP_BG.place(x=0, y=0, relwidth=1, relheight=1)
            useridS = StringVar()
            passwordS = StringVar()
            re_passwordS = StringVar()
            add_user_type = StringVar()
            add_user_type.set("NULL")

            add_userid_label = Label(add_user_top, text="Username", font=("Goudy old style", 15, "bold"), fg="black",bg="white")
            add_useridE = Entry(add_user_top, textvariable=useridS, font=("times new roman", 15), bg="light grey")
            add_password_label = Label(add_user_top, text="Password", font=("Goudy old style", 15, "bold"), fg="black",bg="white")
            add_passwordE = Entry(add_user_top, show="*", textvariable=passwordS, font=("times new roman", 15),bg="light grey")
            add_repassword = Label(add_user_top, text="Re-Password", font=("Goudy old style", 15, "bold"), fg="black",bg="white")
            add_repasswordE = Entry(add_user_top, show="*", textvariable=re_passwordS, font=("times new roman", 15),bg="light grey")
            add_label_usertype = Label(add_user_top, text="User Type", font=("Goudy old style", 15, "bold"), fg="black",bg="white")
            admin_radio_button = Radiobutton(add_user_top, text="ADMIN",font=("Goudy old style", 15, "bold"),bg="white", variable=add_user_type, value="ADMIN")
            user_radio_button = Radiobutton(add_user_top,text= "USER",font=("Goudy old style", 15, "bold"),bg="white", variable=add_user_type, value="USER")
            add_button = Button(add_user_top, command=add, text="Add", fg="black", bg="sky blue",font=("times new roman", 15))
            cancel_button = Button(add_user_top, command=add_user_top.destroy, text="Cancel", fg="black", bg="sky blue", font=("times new roman", 15))

            add_userid_label.place(x=20, y=20)
            add_useridE.place(x=175, y=20, width=350, height=30)
            add_password_label.place(x=20, y=60)
            add_passwordE.place(x=175, y=60, width=350, height=30)
            add_repassword.place(x=20, y=100)
            add_repasswordE.place(x=175, y=100, width=350, height=30)
            add_label_usertype.place(x=20, y=140)
            admin_radio_button.place(x=175, y=140)
            user_radio_button.place(x=300, y=140)
            add_button.place(x=150, y=220, height=30, width=80)
            cancel_button.place(x=350, y=220, height=30, width=80)

        def delete_user():
            sel_row = table_admin.selection()
            if(len(sel_row)==1):
                user_sel= table_admin.item(sel_row,'values')
                value = tmg.askquestion("Delete", "Do you want to delete "+str(user_sel[0])+" ?")
                if (value == 'yes'):
                    c.execute("DELETE from USER WHERE USER_ID = :name", {'name': str(user_sel[0])})
                    conn.commit()
                    table_admin.delete(sel_row)
            elif(len(sel_row)>1):
                no_of_user= len(sel_row)
                value = tmg.askquestion("Delete", "Do you want to delete "+str(no_of_user)+" users ?")
                if (value == 'yes'):
                    for record in sel_row:
                        user_sel=table_admin.item(record,'values')
                        c.execute("DELETE from USER WHERE USER_ID = :name", {'name': str(user_sel[0])})
                        conn.commit()
                        table_admin.delete(record)

        def update_user():
            def update():
                if(update_passwordE.get() =="" and update_repasswordE.get() ==""):
                    global curr_date
                    curr_date = str(datetime.datetime.now().replace(second=0, microsecond=0))
                    table_admin.item(sel_row,text=str(sel_row[0]),values= (user_sel[0],update_user_type.get(),curr_date))
                    current_user_type = update_user_type.get()
                    c.execute("UPDATE USER set USER_TYPE = :type, ENTRY_DATE = :date WHERE USER_ID = :name", {'name': str(user_sel[0]),'type': current_user_type,'date': curr_date})
                    conn.commit()
                    update_user_top.destroy()
                elif(update_passwordE.get() != update_repasswordE.get()):
                    tmg.showwarning("Error", "Please check Password and Re-Password !", parent=update_user_top)
                elif((update_passwordE.get() == update_repasswordE.get()) and (len(update_passwordE.get())>0) and (len(update_repasswordE.get())>0)):
                    curr_date = str(datetime.datetime.now().replace(second=0, microsecond=0))
                    table_admin.item(sel_row, text=str(sel_row[0]),values=(user_sel[0], update_user_type.get(), curr_date))
                    current_user_type = update_user_type.get()
                    update_password = update_passwordE.get()
                    salt = bcrypt.gensalt()
                    test = bcrypt.hashpw(update_password.encode(), salt)
                    c.execute("UPDATE USER set USER_TYPE = :type, PASSWORD = :test, ENTRY_DATE = :date WHERE USER_ID = :name",{'name': str(user_sel[0]),'type': current_user_type, 'test': test, 'date': curr_date})
                    conn.commit()
                    update_user_top.destroy()

            sel_row = table_admin.selection()
            if (len(sel_row) > 1):
                tmg.showwarning("Error", "Please select One user !", parent=Frame_right)
            elif(len(sel_row)==0):
                tmg.showwarning("Error", "Please select One user to update !", parent=Frame_right)
            else:
                user_sel = table_admin.item(sel_row, 'values')
                update_user_top = Toplevel(Frame_right, bg="white")
                update_user_top.title("Update User")
                update_user_top.geometry("600x300+0+0")
                update_user_top.resizable(False, False)
                TOP_BG = Label(update_user_top, image=bgtop1)
                TOP_BG.place(x=0, y=0, relwidth=1, relheight=1)

                passwordS = StringVar()
                re_passwordS = StringVar()
                update_user_type = StringVar()
                update_user_type.set(str(user_sel[1]))

                update_userid = Label(update_user_top, text="Username", font=("Goudy old style", 15, "bold"), fg="black",bg="white")
                update_useridE = Label(update_user_top, text=str(user_sel[0]), font=("Goudy old style", 15, "bold"), fg="black", bg="white")
                update_password = Label(update_user_top, text="Password", font=("Goudy old style", 15, "bold"), fg="black",bg="white")
                update_passwordE = Entry(update_user_top, show="*", textvariable=passwordS, font=("times new roman", 15),bg="light grey")
                update_repassword = Label(update_user_top, text="Re-Password", font=("Goudy old style", 15, "bold"), fg="black",bg="white")
                update_repasswordE = Entry(update_user_top, show="*", textvariable=re_passwordS, font=("times new roman", 15),bg="light grey")
                update_lbl_usertype = Label(update_user_top, text="User Type", font=("Goudy old style", 15, "bold"), fg="black",bg="white")
                admin_radiobutton = Radiobutton(update_user_top, text="ADMIN", font=("Goudy old style", 15, "bold"),bg="white", variable=update_user_type, value="ADMIN")
                user_radiobutton = Radiobutton(update_user_top, text="USER", font=("Goudy old style", 15, "bold"), bg="white",variable=update_user_type, value="USER")
                update_button = Button(update_user_top,command=update, text="Update", fg="black", bg="sky blue",font=("times new roman", 15))
                cancel_button = Button(update_user_top, command=update_user_top.destroy, text="Cancel", fg="black",bg="sky blue", font=("times new roman", 15))

                update_userid.place(x=20, y=20)
                update_useridE.place(x=175, y=20)
                update_password.place(x=20, y=60)
                update_passwordE.place(x=175, y=60, width=350, height=30)
                update_repassword.place(x=20, y=100)
                update_repasswordE.place(x=175, y=100, width=350, height=30)
                update_lbl_usertype.place(x=20, y=140)
                admin_radiobutton.place(x=175, y=140)
                user_radiobutton.place(x=300, y=140)
                update_button.place(x=150, y=220, height=30, width=80)
                cancel_button.place(x=350, y=220, height=30, width=80)

        global Frame_right
        Frame_right.destroy()
        Frame_right = Frame(root)
        Frame_right.place(x=350, y=60, height=600, width=900)
        FR_BG = Label(Frame_right, image=bg3)
        FR_BG.place(x=0, y=0, relwidth=1, relheight=1)

        add_button= Button(Frame_right,command=add_user, text="Add", fg="black", bg="sky blue", font=("times new roman", 15))
        update_button = Button(Frame_right,command=update_user, text="Update", fg="black", bg="sky blue", font=("times new roman", 15))
        del_button = Button(Frame_right,command=delete_user, text="Delete", fg="black", bg="sky blue", font=("times new roman", 15))

        add_button.place(x=650, y=160, height=50, width=100)
        update_button.place(x=650, y=260, height=50, width=100)
        del_button.place(x=650, y=360, height=50, width=100)

        Frame_adminport = Frame(Frame_right, bg="grey")
        Frame_adminport.place(x=40, y=110, height=370, width=510)

        table_admin_yscroll= Scrollbar(Frame_adminport)
        table_admin_yscroll.pack(side=RIGHT,fill=Y)

        table_admin = ttk.Treeview(Frame_adminport,height=17,yscrollcommand=table_admin_yscroll.set)
        table_admin.pack()
        table_admin_yscroll.config(command=table_admin.yview)
        table_admin['columns'] = ("User ID", "Entry By","Entry Date")
        table_admin['show'] = 'headings'
        table_admin.column("#0",anchor=W,width =0,stretch=NO)
        table_admin.column("User ID",anchor=W,width=220)
        table_admin.column("Entry By",anchor=CENTER,width=120)
        table_admin.column("Entry Date",anchor=W,width=150)

        table_admin.heading("#0",text="#", anchor=W)
        table_admin.heading("User ID", text="User ID", anchor=W)
        table_admin.heading("Entry By",text="Entry By",anchor=CENTER)
        table_admin.heading("Entry Date",text="Entry Date",anchor=W)

        c.execute("SELECT USER_ID, USER_TYPE, ENTRY_DATE FROM USER")
        data = c.fetchall()
        global count
        count =0
        for record in data:
            table_admin.insert(parent='', index='end', iid=count, text=(count + 1),values=(record[0], record[1], record[2]))
            count += 1

        table_admin.pack()
        table_admin.place(x=0,y=0)

    def view_portal():
        def comboclick(event):
            if(sel_classD.get() in ["XI", "XII"]):
                section_label.configure(text="Stream")
                sel_secD.configure(value=["Arts", "Commerce", "Science"])
                sel_secD.current(0)
            else:
                section_label.configure(text="Section")
                sel_secD.configure(value=["A", "B", "C"])
                sel_secD.current(0)

        def view_go():
            def view_personal_details():
                sel_row = class_view_tree.selection()
                if (len(sel_row) > 1):
                    tmg.showwarning("Error", "Please select One Student !", parent=Frame_right)
                elif (len(sel_row) == 0):
                    tmg.showwarning("Error", "Please select One Student to view personal details !", parent=Frame_right)
                else:
                    user_sel = class_view_tree.item(sel_row, 'values')
                    viewpdetail_top = Toplevel(Frame_right)
                    viewpdetail_top.title("View Personal Details")
                    viewpdetail_top.geometry("900x600+0+0")
                    viewpdetail_top.resizable(False, False)
                    TOP_BG = Label(viewpdetail_top, image=bgtop2)
                    TOP_BG.place(x=0, y=0, relwidth=1, relheight=1)

                    studentnameS = StringVar()
                    studentnameS.set(str(user_sel[1]))
                    opt_subS= StringVar()
                    rollS = StringVar()
                    dob_dateS = StringVar()
                    dob_monthS = StringVar()
                    dob_yearS = StringVar()
                    genderS = StringVar()
                    guardian_nameS = StringVar()
                    addressT = StringVar()

                    index = roll.index(int(user_sel[0]))
                    dob_date = data[index][4]
                    dob_month = data[index][5]
                    dob_year = data[index][6]
                    gender = data[index][7]
                    guardian_name = data[index][8]
                    address = data[index][9]
                    rollS.set(str(user_sel[0]))
                    dob_dateS.set(str(dob_date))
                    dob_monthS.set(str(dob_month))
                    dob_yearS.set(str(dob_year))
                    genderS.set(gender)
                    guardian_nameS.set(guardian_name)
                    addressT.set(address)

                    name_lbl = Label(viewpdetail_top, text="Name", font=("Goudy old style", 15, "bold"), fg="black")
                    studentname_lbl = Label(viewpdetail_top, text=str(user_sel[1]),font=("Goudy old style", 15, "bold"), fg="black")
                    class_r_lbl = Label(viewpdetail_top, text=("Class   "+str(sel_classS.get())), font=("Goudy old style", 15, "bold"),fg="black")

                    name_lbl.place(x=20, y=20)
                    studentname_lbl.place(x=200, y=20)
                    class_r_lbl.place(x=20, y=60)

                    if(class_roman_to_numerical[sel_classS.get()]==11 or class_roman_to_numerical[sel_classS.get()]==12):
                        opt_sub = data[index][10]
                        opt_subS.set(opt_sub)
                        section_label = Label(viewpdetail_top, text="Stream", font=("Goudy old style", 15, "bold"),fg="black")
                        sec_r_lbl = Label(viewpdetail_top, text=str(sel_sectionS.get()),font=("Goudy old style", 15, "bold"), fg="black")
                        opt_sub_lbl = Label(viewpdetail_top, text="Optional Subject", font=("Goudy old style", 15, "bold"),fg="black")
                        opt_r_sub_lbl = Label(viewpdetail_top, text=str(opt_subS.get()),font=("Goudy old style", 15, "bold"), fg="black")
                        section_label.place(x=200, y=60)
                        sec_r_lbl.place(x=280, y=60)
                        opt_sub_lbl.place(x=450, y=60)
                        opt_r_sub_lbl.place(x=600, y=60)
                    else:
                        section_label = Label(viewpdetail_top, text="Section", font=("Goudy old style", 15, "bold"),fg="black")
                        sec_r_lbl = Label(viewpdetail_top, text=str(sel_sectionS.get()),font=("Goudy old style", 15, "bold"), fg="black")
                        section_label.place(x=120, y=60)
                        sec_r_lbl.place(x=200, y=60)
                    roll_label= Label(viewpdetail_top, text="Roll No.", font=("Goudy old style", 15, "bold"),fg="black")
                    roll_r_lbl= Label(viewpdetail_top, text=str(rollS.get()),font=("Goudy old style", 15, "bold"), fg="black")
                    dob_label= Label(viewpdetail_top, text="Date of birth", font=("Goudy old style", 15, "bold"),fg="black")
                    dob_r_lbl= Label(viewpdetail_top, text=(str(dob_dateS.get())+" / "+dob_monthS.get()+" / "+dob_yearS.get()),font=("Goudy old style", 15, "bold"), fg="black")
                    gender_label = Label(viewpdetail_top, text="Gender", font=("Goudy old style", 15, "bold"),fg="black")
                    gender_r_lbl =Label(viewpdetail_top, text=str(genderS.get()),font=("Goudy old style", 15, "bold"), fg="black")
                    guardian_lbl= Label(viewpdetail_top, text="Guardain's Name", font=("Goudy old style", 15, "bold"),fg="black")
                    guardian_r_lbl= Label(viewpdetail_top, text=str(guardian_nameS.get()),font=("Goudy old style", 15, "bold"), fg="black")
                    address_label = Label(viewpdetail_top, text="Address", font=("Goudy old style", 15, "bold"),fg="black")
                    address_r_lbl = Label(viewpdetail_top, text=str(addressT.get()),font=("Goudy old style", 15, "bold"), fg="black")
                    cancel_button = Button(viewpdetail_top, command=viewpdetail_top.destroy, text="Cancel", fg="black",bg="sky blue", font=("times new roman", 15))
                    roll_label.place(x=20, y=100)
                    roll_r_lbl.place(x=200, y=100)
                    dob_label.place(x=20, y=140)
                    dob_r_lbl.place(x=200, y=140)
                    gender_label.place(x=20, y=180)
                    gender_r_lbl.place(x=200, y=180)
                    guardian_lbl.place(x=20, y=220)
                    guardian_r_lbl.place(x=200, y=220)
                    address_label.place(x=20, y=260)
                    address_r_lbl.place(x=200, y=260)
                    cancel_button.place(x=420, y=500)

            def update_personal_details():
                def update():
                    if ((check_date(int(dob_yearS.get()), int(dob_monthS.get()), int(dob_dateS.get()))) == "False"):
                        tmg.showwarning("Error", "Invalid date inserted in Date of Birth !", parent=Frame_right)
                    elif (class_roman_to_numerical[sel_classS.get()] == 11 or class_roman_to_numerical[
                        sel_classS.get()] == 12):
                        class_view_tree.item(sel_row, text=str(sel_row[0]), values=(user_sel[0], studentnameS.get()))
                        c.execute("UPDATE SENIOR set USER_NAME = :name, DOB_DATE = :ddate, DOB_MONTH = :dmonth, DOB_YEAR = :dyear, GENDER = :gender, GUARDIAN_NAME = :gname, ADDRESS = :address WHERE USER_ROLL = :roll",{'roll': str(rollS.get()), 'name': str(studentnameS.get()), 'ddate': str(dob_dateS.get()), 'dmonth': str(dob_monthS.get()), 'dyear': str(dob_yearS.get()), 'gender': str(genderS.get()), 'gname': str(guardian_nameS.get()), 'address': addressT.get(1.0, END)})
                        conn.commit()
                        updatepdetail_top.destroy()
                        view_go()
                    elif(class_roman_to_numerical[sel_classS.get()] >= 5 and class_roman_to_numerical[sel_classS.get()] <= 10):
                        class_view_tree.item(sel_row, text=str(sel_row[0]), values=(user_sel[0], studentnameS.get()))
                        c.execute("UPDATE MIDDLE set USER_NAME = :name, DOB_DATE = :ddate, DOB_MONTH = :dmonth, DOB_YEAR = :dyear, GENDER = :gender, GUARDIAN_NAME = :gname, ADDRESS = :address WHERE USER_ROLL = :roll",{'roll': str(rollS.get()), 'name': str(studentnameS.get()), 'ddate': str(dob_dateS.get()), 'dmonth': str(dob_monthS.get()), 'dyear': str(dob_yearS.get()), 'gender': str(genderS.get()), 'gname': str(guardian_nameS.get()), 'address': addressT.get(1.0, END)})
                        conn.commit()
                        updatepdetail_top.destroy()
                        view_go()
                    else:
                        class_view_tree.item(sel_row, text=str(sel_row[0]), values=(user_sel[0], studentnameS.get()))
                        c.execute("UPDATE JUNIOR set USER_NAME = :name, DOB_DATE = :ddate, DOB_MONTH = :dmonth, DOB_YEAR = :dyear, GENDER = :gender, GUARDIAN_NAME = :gname, ADDRESS = :address WHERE USER_ROLL = :roll",
                            {'roll': str(rollS.get()), 'name': str(studentnameS.get()), 'ddate': str(dob_dateS.get()),
                             'dmonth': str(dob_monthS.get()), 'dyear': str(dob_yearS.get()),
                             'gender': str(genderS.get()), 'gname': str(guardian_nameS.get()),
                             'address': addressT.get(1.0, END)})
                        conn.commit()
                        updatepdetail_top.destroy()
                        view_go()

                sel_row = class_view_tree.selection()
                if (len(sel_row) > 1):
                    tmg.showwarning("Error", "Please select One Student !", parent=Frame_right)
                elif (len(sel_row) == 0):
                    tmg.showwarning("Error", "Please select One Student to update personal details !", parent=Frame_right)
                else:
                    user_sel = class_view_tree.item(sel_row, 'values')
                    updatepdetail_top = Toplevel(Frame_right)
                    updatepdetail_top.title("Update Personal Details")
                    updatepdetail_top.geometry("900x600+0+0")
                    updatepdetail_top.resizable(False, False)
                    TOP_BG = Label(updatepdetail_top, image=bgtop2)
                    TOP_BG.place(x=0, y=0, relwidth=1, relheight=1)

                    studentnameS = StringVar()
                    opt_subS = StringVar()
                    rollS = StringVar()
                    dob_dateS = StringVar()
                    dob_monthS = StringVar()
                    dob_yearS = StringVar()
                    genderS = StringVar()
                    guardian_nameS = StringVar()
                    addressT = StringVar()

                    index = roll.index(int(user_sel[0]))
                    dob_date = data[index][4]
                    dob_month = data[index][5]
                    dob_year = data[index][6]
                    gender = data[index][7]
                    guardian_name = data[index][8]
                    address = data[index][9]
                    studentnameS.set(str(user_sel[1]))
                    rollS.set(str(user_sel[0]))
                    dob_dateS.set(dob_date)
                    dob_monthS.set(dob_month)
                    dob_yearS.set(dob_year)
                    genderS.set(gender)
                    guardian_nameS.set(guardian_name)
                    addressT.set(address)

                    name_lbl = Label(updatepdetail_top, text="Name", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=20)
                    studentname_lbl = Entry(updatepdetail_top, textvariable=studentnameS,font=("times new roman", 15),bg="light grey")
                    studentname_lbl.place(x=250, y=20,width=350, height=30)
                    class_r_lbl = Label(updatepdetail_top, text=("Class   "+str(sel_classS.get())),font=("Goudy old style", 15, "bold"), fg="black").place(x=20, y=60)
                    if (class_roman_to_numerical[sel_classS.get()] == 11 or class_roman_to_numerical[sel_classS.get()] == 12):
                        opt_sub = data[index][10]
                        opt_subS.set(opt_sub)
                        section_label = Label(updatepdetail_top, text="Stream", font=("Goudy old style", 15, "bold"),fg="black").place(x=250, y=60)
                        sec_r_lbl = Label(updatepdetail_top, text=str(sel_sectionS.get()),font=("Goudy old style", 15, "bold"), fg="black").place(x=320, y=60)
                        opt_sub_lbl = Label(updatepdetail_top, text="Optional Subject",font=("Goudy old style", 15, "bold"), fg="black").place(x=500, y=60)
                        opt_r_sub_lbl = Label(updatepdetail_top, text=str(opt_subS.get()),font=("Goudy old style", 15, "bold"), fg="black").place(x=650, y=60)
                    else:
                        section_label = Label(updatepdetail_top, text="Section", font=("Goudy old style", 15, "bold"),fg="black").place(x=250, y=60)
                        sec_r_lbl = Label(updatepdetail_top, text=str(sel_sectionS.get()),font=("Goudy old style", 15, "bold"), fg="black").place(x=350, y=60)
                    roll_label = Label(updatepdetail_top, text="Roll No.", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=100)
                    roll_r_lbl = Label(updatepdetail_top, text=str(rollS.get()), font=("Goudy old style", 15, "bold"),fg="black").place(x=250, y=100)
                    dob_label = Label(updatepdetail_top, text="Date of birth", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=140)
                    dob_dateD = ttk.Combobox(updatepdetail_top, textvariable=dob_dateS, font=(15),value=[x for x in range(1, 32)], state="readonly")
                    dob_dateD.place(x=250, y=140, width=50, height=30)
                    slash_label = Label(updatepdetail_top, text="/                /", font=("Goudy old style", 15, "bold"),fg="black").place(x=315, y=140)
                    dob_monthD = ttk.Combobox(updatepdetail_top, textvariable=dob_monthS, font=(15),value=[y for y in range(1, 13)], state="readonly")
                    dob_monthD.place(x=340, y=140,width=50,height=30)
                    dob_yearD = ttk.Combobox(updatepdetail_top, textvariable=dob_yearS, font=(15),value=[z for z in range(2020, 1980, -1)], state="readonly")
                    dob_yearD.place(x=430,y=140,width=90,height=30)
                    gender_label = Label(updatepdetail_top, text="Gender", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=180)
                    select_genderD = ttk.Combobox(updatepdetail_top, textvariable=genderS, font=(15), value=["Male", "Female"],state="readonly")
                    select_genderD.place(x=250, y=180, width=90, height=30)
                    guardian_name_label = Label(updatepdetail_top, text="Guardian's Name", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=220)
                    guardian_name_entrybox = Entry(updatepdetail_top, textvariable=guardian_nameS, font=("times new roman", 15),bg="light grey")
                    guardian_name_entrybox.place(x=250, y=220, width=350, height=30)
                    address_label = Label(updatepdetail_top, text="Address", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=260)
                    addressT = ScrolledText(updatepdetail_top, width=55, height=9, font=("times new roman", 15),bg="light grey")
                    addressT.place(x=250, y=260)
                    addressT.insert(1.0,address)
                    update_button = Button(updatepdetail_top, command=update, text="Update", fg="black", bg="sky blue",font=("times new roman", 15))
                    update_button.place(x=250, y=470, height=30, width=80)
                    cancel_button = Button(updatepdetail_top, command=updatepdetail_top.destroy, text="Cancel", fg="black",bg="sky blue", font=("times new roman", 15))
                    cancel_button.place(x=490, y=470, height=30, width=80)

            def delete():
                if(class_roman_to_numerical[sel_classS.get()] == 11 or class_roman_to_numerical[sel_classS.get()] == 12):
                    sel_row = class_view_tree.selection()
                    if (len(sel_row) == 1):
                        user_sel = class_view_tree.item(sel_row, 'values')
                        value = tmg.askquestion("Delete", "Do you want to delete Roll " + str(user_sel[0]) + " ?")
                        if (value == 'yes'):
                            c.execute("DELETE from SENIOR WHERE USER_ROLL = :roll", {'roll': str(user_sel[0])})
                            conn.commit()
                            class_view_tree.delete(sel_row)
                    elif (len(sel_row) > 1):
                        no_of_user = len(sel_row)
                        value = tmg.askquestion("Delete", "Do you want to delete " + str(no_of_user) + " students ?")
                        if (value == 'yes'):
                            for record in sel_row:
                                user_sel = class_view_tree.item(record, 'values')
                                c.execute("DELETE from SENIOR WHERE USER_ROLL = :roll", {'roll': str(user_sel[0])})
                                conn.commit()
                                class_view_tree.delete(record)
                elif(class_roman_to_numerical[sel_classS.get()] >= 5 and class_roman_to_numerical[sel_classS.get()] <= 10):
                    sel_row = class_view_tree.selection()
                    if (len(sel_row) == 1):
                        user_sel = class_view_tree.item(sel_row, 'values')
                        value = tmg.askquestion("Delete", "Do you want to delete Roll " + str(user_sel[0]) + " ?")
                        if (value == 'yes'):
                            c.execute("DELETE from MIDDLE WHERE USER_ROLL = :roll", {'roll': str(user_sel[0])})
                            conn.commit()
                            class_view_tree.delete(sel_row)
                    elif (len(sel_row) > 1):
                        no_of_user = len(sel_row)
                        value = tmg.askquestion("Delete", "Do you want to delete " + str(no_of_user) + " students ?")
                        if (value == 'yes'):
                            for record in sel_row:
                                user_sel = class_view_tree.item(record, 'values')
                                c.execute("DELETE from MIDDLE WHERE USER_ROLL = :roll", {'roll': str(user_sel[0])})
                                conn.commit()
                                class_view_tree.delete(record)
                elif(class_roman_to_numerical[sel_classS.get()] < 5):
                    sel_row = class_view_tree.selection()
                    if (len(sel_row) == 1):
                        user_sel = class_view_tree.item(sel_row, 'values')
                        value = tmg.askquestion("Delete", "Do you want to delete Roll " + str(user_sel[0]) + " ?")
                        if (value == 'yes'):
                            c.execute("DELETE from JUNIOR WHERE USER_ROLL = :roll", {'roll': str(user_sel[0])})
                            conn.commit()
                            class_view_tree.delete(sel_row)
                    elif (len(sel_row) > 1):
                        no_of_user = len(sel_row)
                        value = tmg.askquestion("Delete", "Do you want to delete " + str(no_of_user) + " students ?")
                        if (value == 'yes'):
                            for record in sel_row:
                                user_sel = class_view_tree.item(record, 'values')
                                c.execute("DELETE from JUNIOR WHERE USER_ROLL = :roll", {'roll': str(user_sel[0])})
                                conn.commit()
                                class_view_tree.delete(record)

            if (sel_classD.get() == "" or sel_secD.get() == ""):
                tmg.showwarning("Error", "All fields are required !", parent=Frame_right)
            else:
                FR_BG.configure(image=bg7)
                class_roman_to_numerical = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
                                            "VI": 6, "VII": 7, "VIII": 8, "IX": 9,
                                            "X": 10, "XI": 11, "XII": 12}

                global check
                check = str(class_roman_to_numerical[sel_classS.get()])

                class_view_tree = ttk.Treeview(Frame_right, height=15)
                class_view_tree.pack()
                class_view_tree_yscroll = ttk.Scrollbar(Frame_right, orient="vertical", command=class_view_tree.yview)
                class_view_tree_yscroll.place(x=480, y=150, height=320)
                class_view_tree.config(yscrollcommand=class_view_tree_yscroll.set)
                class_view_tree.pack()
                class_view_tree['columns'] = ("Roll No.", "Name")
                class_view_tree['show'] = 'headings'
                class_view_tree.column("#0", anchor=W, width=0, stretch=NO)
                class_view_tree.column("Roll No.", anchor=W, width=100)
                class_view_tree.column("Name", anchor=W, width=320)
                class_view_tree.heading("#0", text="#", anchor=W)
                class_view_tree.heading("Roll No.", text="Roll No.", anchor=W)
                class_view_tree.heading("Name", text="Name", anchor=W)
                if (int(check) < 5):
                    c.execute("SELECT JT FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                    d = c.fetchall()
                    if (d[0][0] == 1):
                        c.execute("SELECT * FROM JUNIOR")
                        data = c.fetchall()
                        global count
                        count = 0
                        roll = []
                        for record in data:
                            if(record[1]==class_roman_to_numerical[sel_classS.get()] and record[2]==sel_sectionS.get()):
                                class_view_tree.insert(parent='', index='end', iid=count, text=(count + 1),
                                                   values=(record[3], record[0]))
                                count += 1
                            roll.append(record[3])
                            showing_tree_lbl.configure(text="Showing Data of " + str(count) + " Students of " + str(
                                sel_classD.get()) + " ➖ " + str(sel_secD.get()))
                            showing_tree_lbl.place(x=50, y=120)
                    else:
                        showing_tree_lbl.configure(text="Showing Data of " + str(0) + " Students of " + str(
                            sel_classD.get()) + " ➖ " + str(sel_secD.get()))
                        showing_tree_lbl.place(x=50, y=120)

                elif ((int(check) >= 5) and (int(check) <= 10)):
                    c.execute("SELECT MT FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                    d = c.fetchall()
                    if(d[0][0] == 1):
                        c.execute("SELECT * FROM MIDDLE")
                        data = c.fetchall()
                        count = 0
                        roll = []
                        for record in data:
                            if(record[1]==class_roman_to_numerical[sel_classS.get()] and record[2]==sel_sectionS.get()):
                                class_view_tree.insert(parent='', index='end', iid=count, text=(count + 1),
                                       values=(record[3], record[0]))
                                count += 1
                            roll.append(record[3])
                            showing_tree_lbl.configure(text="Showing Data of " + str(count) + " Students of " + str(
                                sel_classD.get()) + " ➖ " + str(sel_secD.get()))
                            showing_tree_lbl.place(x=50, y=120)
                    else:
                        showing_tree_lbl.configure(text="Showing Data of " + str(0) + " Students of " + str(
                            sel_classD.get()) + " ➖ " + str(sel_secD.get()))
                        showing_tree_lbl.place(x=50, y=120)
                else:
                    c.execute("SELECT ST FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                    d = c.fetchall()
                    if(d[0][0] == 1):
                        c.execute("SELECT * FROM SENIOR")
                        data = c.fetchall()
                        count = 0
                        roll = []
                        for record in data:
                            if(record[1]==class_roman_to_numerical[sel_classS.get()] and record[2]==sel_sectionS.get()):
                                class_view_tree.insert(parent='', index='end', iid=count, text=(count + 1),
                                       values=(record[3], record[0]))
                                count += 1
                            roll.append(record[3])
                            showing_tree_lbl.configure(text="Showing Data of " + str(count) + " Students of " + str(
                                sel_classD.get()) + " ➖ " + str(sel_secD.get()))
                            showing_tree_lbl.place(x=50, y=120)
                    else:
                        showing_tree_lbl.configure(text="Showing Data of " + str(0) + " Students of " + str(
                            sel_classD.get()) + " ➖ " + str(sel_secD.get()))
                        showing_tree_lbl.place(x=50, y=120)
                class_view_tree.pack()
                class_view_tree.place(x=50, y=150)

                view_personal_details_button = Button(Frame_right,command=view_personal_details, text="View Personal Details", fg="white", bg="#d77337",font=("times new roman", 15))
                view_personal_details_button.place(x=600, y=200, height=35, width=200)
                update_personal_details_button = Button(Frame_right,command=update_personal_details, text="Update Personal Details", fg="white", bg="#d77337",font=("times new roman", 15))
                update_personal_details_button.place(x=600, y=300, height=35, width=200)
                del_button = Button(Frame_right,command=delete, text="DELETE", fg="white", bg="#d77337",font=("times new roman", 15))
                del_button.place(x=600, y=400, height=35, width=200)

        global Frame_right
        Frame_right.destroy()
        Frame_right = Frame(root)
        Frame_right.place(x=350, y=60, height=600, width=900)
        FR_BG = Label(Frame_right, image=bg6)
        FR_BG.place(x=0, y=0, relwidth=1, relheight=1)

        r_class = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII","IX", "X", "XI", "XII"]
        sel_classS= StringVar()
        sel_sectionS= StringVar()

        class_lbl = Label(Frame_right, text="Class", font=("Goudy old style", 20, "bold"), fg="black")
        class_lbl.place(x=150, y=65)
        sel_classD = ttk.Combobox(Frame_right, textvariable=sel_classS, font=(20), value=r_class, state="readonly")
        sel_classD.place(x=250, y=65, width=100, height=35)
        sel_classD.current(0)
        section_label = Label(Frame_right, text="Section", font=("Goudy old style", 20, "bold"), fg="black")
        section_label.place(x=400, y=65)
        sel_secD = ttk.Combobox(Frame_right, textvariable=sel_sectionS, font=(25), state="readonly")
        sel_secD.place(x=500, y=65, width=100, height=35)
        sel_secD.configure(value=["A", "B", "C"])
        sel_secD.current(0)
        sel_classD.bind("<<ComboboxSelected>>", comboclick)
        showing_tree_lbl = Label(Frame_right, font=("Goudy old style", 15, "bold"), fg="black")
        go_bt = Button(Frame_right,command=view_go, text="GO➡", fg="black", bg="sky blue", font=("times new roman", 15))
        go_bt.place(x=700, y=65, height=35, width=100)

    def data_entry():

        def entry_class(class_no,roman_classno):
            if(class_no < 5):
                c.execute("""CREATE TABLE IF NOT EXISTS JUNIOR (
                             USER_NAME VARCHAR(100) NOT NULL,
                             USER_CLASS INTEGER NOT NULL,
                             USER_SEC VARCHAR(5) NOT NULL,
                             USER_ROLL INTEGER PRIMARY KEY NOT NULL,
                             DOB_DATE INTEGER NOT NULL,
                             DOB_MONTH INTEGER NOT NULL,
                             DOB_YEAR INTEGER NOT NULL,
                             GENDER VARCHAR(20) NOT NULL,
                             GUARDIAN_NAME VARCHAR(100) NOT NULL,
                             ADDRESS VARCHAR(255) NOT NULL,
                             BENGALI_UNIT INTEGER,
                             BENGALI_HALF INTEGER,
                             BENGALI_FINAL INTEGER,
                             ENGLISH_UNIT INTEGER,
                             ENGLISH_HALF INTEGER,
                             ENGLISH_FINAL INTEGER,
                             MATH_UNIT INTEGER,
                             MATH_HALF INTEGER,
                             MATH_FINAL INTEGER,
                             GK_UNIT INTEGER,
                             GK_HALF INTEGER,
                             GK_FINAL INTEGER
                             );""")
            elif((class_no >=5) and (class_no <= 10)):
                c.execute("""CREATE TABLE IF NOT EXISTS MIDDLE (
                             USER_NAME VARCHAR(100) NOT NULL,
                             USER_CLASS INTEGER NOT NULL,
                             USER_SEC VARCHAR(5) NOT NULL,
                             USER_ROLL INTEGER PRIMARY KEY NOT NULL,
                             DOB_DATE INTEGER NOT NULL,
                             DOB_MONTH INTEGER NOT NULL,
                             DOB_YEAR INTEGER NOT NULL,
                             GENDER VARCHAR(20) NOT NULL,
                             GUARDIAN_NAME VARCHAR(100) NOT NULL,
                             ADDRESS VARCHAR(255) NOT NULL,
                             BENGALI_UNIT INTEGER,
                             BENGALI_HALF INTEGER,
                             BENGALI_FINAL INTEGER,
                             ENGLISH_UNIT INTEGER,
                             ENGLISH_HALF INTEGER,
                             ENGLISH_FINAL INTEGER,
                             MATH_UNIT INTEGER,
                             MATH_HALF INTEGER,
                             MATH_FINAL INTEGER,
                             HISTORY_UNIT INTEGER,
                             HISTORY_HALF INTEGER,
                             HISTORY_FINAL INTEGER,
                             GEOGRAPHY_UNIT INTEGER,
                             GEOGRAPHY_HALF INTEGER,
                             GEOGRAPHY_FINAL INTEGER,
                             PHYS_UNIT INTEGER,
                             PHYS_HALF INTEGER,
                             PHYS_FINAL INTEGER,
                             LIFE_UNIT INTEGER,
                             LIFE_HALF INTEGER,
                             LIFE_FINAL INTEGER
                             );""")
            else:
                c.execute("""CREATE TABLE IF NOT EXISTS SENIOR (
                             USER_NAME VARCHAR(100) NOT NULL,
                             USER_CLASS INTEGER NOT NULL,
                             USER_STREAM VARCHAR(20) NOT NULL,
                             USER_ROLL INTEGER PRIMARY KEY NOT NULL,
                             DOB_DATE INTEGER NOT NULL,
                             DOB_MONTH INTEGER NOT NULL,
                             DOB_YEAR INTEGER NOT NULL,
                             GENDER VARCHAR(20) NOT NULL,
                             GUARDIAN_NAME VARCHAR(100) NOT NULL,
                             ADDRESS VARCHAR(255) NOT NULL,
                             OPTIONAL VARCHAR(20) NOT NULL,
                             BENGALI_UNIT INTEGER,
                             BENGALI_HALF INTEGER,
                             BENGALI_FINAL INTEGER,
                             ENGLISH_UNIT INTEGER,
                             ENGLISH_HALF INTEGER,
                             ENGLISH_FINAL INTEGER,
                             HISTORY_UNIT INTEGER,
                             HISTORY_HALF INTEGER,
                             HISTORY_FINAL INTEGER,
                             PHILOSOPHY_UNIT INTEGER,
                             PHILOSOPHY_HALF INTEGER,
                             PHILOSOPHY_FINAL INTEGER,
                             GEOGRAPHY_UNIT INTEGER,
                             GEOGRAPHY_HALF INTEGER,
                             GEOGRAPHY_FINAL INTEGER,
                             EDUCATION_UNIT INTEGER,
                             EDUCATION_HALF INTEGER,
                             EDUCATION_FINAL INTEGER,
                             POLITICAL_UNIT INTEGER,
                             POLITICAL_HALF INTEGER,
                             POLITICAL_FINAL INTEGER,
                             BUSINESS_UNIT INTEGER,
                             BUSINESS_HALF INTEGER,
                             BUSINESS_FINAL INTEGER,
                             ECONOMICS_UNIT INTEGER,
                             ECONOMICS_HALF INTEGER,
                             ECONOMICS_FINAL INTEGER,
                             ACCOUNT_UNIT INTEGER,
                             ACCOUNT_HALF INTEGER,
                             ACCOUNT_FINAL INTEGER,
                             LAW_UNIT INTEGER,
                             LAW_HALF INTEGER,
                             LAW_FINAL INTEGER,
                             COMA_UNIT INTEGER,
                             COMA_HALF INTEGER,
                             COMA_FINAL INTEGER,
                             PHYSICS_UNIT INTEGER,
                             PHYSICS_HALF INTEGER,
                             PHYSICS_FINAL INTEGER,
                             CHEMISTRY_UNIT INTEGER,
                             CHEMISTRY_HALF INTEGER,
                             CHEMISTRY_FINAL INTEGER,
                             MATH_UNIT INTEGER,
                             MATH_HALF INTEGER,
                             MATH_FINAL INTEGER,
                             BIOLOGY_UNIT INTEGER,
                             BIOLOGY_HALF INTEGER,
                             BIOLOGY_FINAL INTEGER,
                             COMS_UNIT INTEGER,
                             COMS_HALF INTEGER,
                             COMS_FINAL INTEGER
                             );""")

            def entry_add():
                if ((class_no > 10) and (name_entrybox.get()=="" or section_selS.get()=="" or roll_entry.get()=="" or dob_dateS.get()=="" or dob_monthS.get()=="" or dob_yearS.get()=="" or genderS.get()=="" or guardian_name_entrybox.get()=="" or adress_textboxT.get(1.0,'end-1c')=="" or select_optional_subS=="")):
                    tmg.showwarning("Error", "All fields are required !", parent=Frame_right)
                elif((class_no <= 10) and (name_entrybox.get()=="" or section_selS.get()=="" or roll_entry.get()=="" or dob_dateS.get()=="" or dob_monthS.get()=="" or dob_yearS.get()=="" or genderS.get()=="" or guardian_name_entrybox.get()=="" or adress_textboxT.get(1.0,'end-1c')=="")):
                    tmg.showwarning("Error", "All fields are required !", parent=Frame_right)
                elif (roll_entry.get().isdigit() == False):
                    tmg.showwarning("Error", "Please check Roll No.!\n Only Integer values are accepted !",parent=Frame_right)
                elif ((check_date(int(dob_yearS.get()), int(dob_monthS.get()), int(dob_dateS.get()))) == "False"):
                    tmg.showwarning("Error", "Invalid date inserted in Date of Birth !", parent=Frame_right)
                else:
                    if(len(data) == 0):
                        value = tmg.askquestion("Add", "Do you want to add " + str(name_entrybox.get()) + " in " + roman_classno + " - " + str(section_selS.get()) + " ?")
                        if (value == 'yes'):
                            if(class_no>10):
                                global st
                                st = 1
                                c.execute("UPDATE USER set ST = :st WHERE USER_ID = :name",{'name': str(user_data[0]), 'st': 1})
                                c.execute("INSERT INTO SENIOR(USER_NAME, USER_CLASS, USER_STREAM, USER_ROLL, DOB_DATE, DOB_MONTH, DOB_YEAR, GENDER, GUARDIAN_NAME, ADDRESS, OPTIONAL, BENGALI_UNIT, BENGALI_HALF, BENGALI_FINAL, ENGLISH_UNIT, ENGLISH_HALF, ENGLISH_FINAL, HISTORY_UNIT, HISTORY_HALF, HISTORY_FINAL, PHILOSOPHY_UNIT, PHILOSOPHY_HALF, PHILOSOPHY_FINAL, GEOGRAPHY_UNIT, GEOGRAPHY_HALF, GEOGRAPHY_FINAL, EDUCATION_UNIT, EDUCATION_HALF, EDUCATION_FINAL, POLITICAL_UNIT, POLITICAL_HALF, POLITICAL_FINAL, BUSINESS_UNIT, BUSINESS_HALF, BUSINESS_FINAL, ECONOMICS_UNIT, ECONOMICS_HALF, ECONOMICS_FINAL, ACCOUNT_UNIT, ACCOUNT_HALF, ACCOUNT_FINAL, LAW_UNIT, LAW_HALF, LAW_FINAL, COMA_UNIT, COMA_HALF, COMA_FINAL, PHYSICS_UNIT, PHYSICS_HALF, PHYSICS_FINAL, CHEMISTRY_UNIT, CHEMISTRY_HALF, CHEMISTRY_FINAL, MATH_UNIT, MATH_HALF, MATH_FINAL, BIOLOGY_UNIT, BIOLOGY_HALF, BIOLOGY_FINAL, COMS_UNIT, COMS_HALF, COMS_FINAL) \
                                            VALUES (:name, :class, :stream, :roll, :ddate, :dmonth, :dyear, :gender, :gname, :address, :optional, :benu, :benh, :benf, :engu, :engh, :engf, :hisu, :hish, :hisf, :phiu, :phih, :phif, :geou, :geoh, :geof, :eduu, :eduh, :eduf, :polu, :polh, :polf, :busu, :bush, :busf, :ecou, :ecoh, :ecof, :accu, :acch, :accf, :lawu, :lawh, :lawf, :comau, :comah, :comaf, :physu, :physh, :physf, :chemu, :chemh, :chemf, :mathu, :mathh, :mathf, :biou, :bioh, :biof, :comsu, :comsh, :comsf)",
                                             {'name': name_entrybox.get(), 'class': str(class_no), 'stream': section_selS.get(),
                                              'roll': roll_entry.get(), 'ddate': str(dob_dateS.get()),
                                              'dmonth': str(dob_monthS.get()), 'dyear': str(dob_yearS.get()), 'gender': genderS.get(),
                                              'gname': guardian_name_entrybox.get(), 'address': adress_textboxT.get(1.0, END), 'optional': select_optional_subS.get(), 'benu': 0, 'benh': 0, 'benf': 0, 'engu': 0, 'engh': 0, 'engf': 0,
                                              'hisu': 0, 'hish': 0, 'hisf': 0, 'phiu': 0, 'phih': 0, 'phif': 0, 'geou': 0, 'geoh': 0, 'geof': 0, 'eduu': 0, 'eduh': 0,'eduf': 0, 'polu': 0, 'polh': 0, 'polf': 0,
                                              'busu': 0, 'bush': 0, 'busf': 0, 'ecou': 0, 'ecoh': 0, 'ecof': 0, 'accu': 0, 'acch': 0, 'accf': 0, 'lawu': 0, 'lawh': 0, 'lawf': 0, 'comau': 0, 'comah': 0, 'comaf': 0,
                                              'physu': 0, 'physh': 0, 'physf': 0, 'chemu': 0, 'chemh': 0, 'chemf': 0, 'mathu': 0, 'mathh': 0, 'mathf': 0, 'biou': 0, 'bioh': 0, 'biof': 0, 'comsu': 0, 'comsh': 0, 'comsf': 0})
                                conn.commit()
                                data_entry()

                            elif((class_no >=5) and (class_no <= 10)):
                                global mt
                                mt = 1
                                c.execute("UPDATE USER set MT = :mt WHERE USER_ID = :name",
                                          {'name': str(user_data[0]), 'mt': 1})
                                c.execute("INSERT INTO MIDDLE(USER_NAME, USER_CLASS, USER_SEC, USER_ROLL, DOB_DATE, DOB_MONTH, DOB_YEAR, GENDER, GUARDIAN_NAME, ADDRESS, BENGALI_UNIT, BENGALI_HALF, BENGALI_FINAL, ENGLISH_UNIT, ENGLISH_HALF, ENGLISH_FINAL, MATH_UNIT, MATH_HALF, MATH_FINAL, HISTORY_UNIT, HISTORY_HALF, HISTORY_FINAL, GEOGRAPHY_UNIT, GEOGRAPHY_HALF, GEOGRAPHY_FINAL, PHYS_UNIT, PHYS_HALF, PHYS_FINAL, LIFE_UNIT, LIFE_HALF, LIFE_FINAL) \
                                            VALUES (:name, :class, :sec, :roll, :ddate, :dmonth, :dyear, :gender, :gname, :address, :benu, :benh, :benf, :engu, :engh, :engf, :mathu, :mathh, :mathf, :hisu, :hish, :hisf, :geou, :geoh, :geof, :phyu, :phyh, :phyf, :lifu, :lifh, :liff)",
                                                {'name': name_entrybox.get(), 'class': str(class_no),
                                                 'sec': section_selS.get(), 'roll': roll_entry.get(),
                                                 'ddate': str(dob_dateS.get()), 'dmonth': str(dob_monthS.get()),
                                                 'dyear': str(dob_yearS.get()), 'gender': genderS.get(),
                                                 'gname': guardian_name_entrybox.get(), 'address': adress_textboxT.get(1.0, END), 'benu': 0, 'benh': 0, 'benf': 0, 'engu': 0, 'engh': 0, 'engf': 0, 'mathu': 0, 'mathh': 0, 'mathf': 0, 'hisu': 0, 'hish': 0, 'hisf': 0, 'geou': 0, 'geoh': 0, 'geof': 0, 'phyu': 0, 'phyh': 0, 'phyf': 0, 'lifu': 0, 'lifh': 0, 'liff': 0})
                                conn.commit()
                                data_entry()
                            else:
                                global jt
                                jt = 1
                                c.execute("UPDATE USER set JT = :jt WHERE USER_ID = :name",
                                          {'name': str(user_data[0]), 'jt': 1})
                                c.execute("INSERT INTO JUNIOR(USER_NAME, USER_CLASS, USER_SEC, USER_ROLL, DOB_DATE, DOB_MONTH, DOB_YEAR, GENDER, GUARDIAN_NAME, ADDRESS, BENGALI_UNIT, BENGALI_HALF, BENGALI_FINAL, ENGLISH_UNIT, ENGLISH_HALF, ENGLISH_FINAL, MATH_UNIT, MATH_HALF, MATH_FINAL, GK_UNIT, GK_HALF, GK_FINAL) \
                                            VALUES (:name, :class, :sec, :roll, :ddate, :dmonth, :dyear, :gender, :gname, :address, :benu, :benh, :benf, :engu, :engh, :engf, :mathu, :mathh, :mathf, :gku, :gkh, :gkf)",
                                                {'name': name_entrybox.get(), 'class': str(class_no),
                                                 'sec': section_selS.get(), 'roll': roll_entry.get(),
                                                 'ddate': str(dob_dateS.get()), 'dmonth': str(dob_monthS.get()),
                                                 'dyear': str(dob_yearS.get()), 'gender': genderS.get(),
                                                 'gname': guardian_name_entrybox.get(), 'address': adress_textboxT.get(1.0, END), 'benu': 0, 'benh': 0, 'benf': 0, 'engu': 0, 'engh': 0, 'engf': 0, 'mathu': 0, 'mathh': 0, 'mathf': 0, 'gku': 0, 'gkh': 0, 'gkf': 0})
                                conn.commit()
                                data_entry()
                    elif(len(data) > 0):
                        if (int(roll_entry.get()) in roll):
                            tmg.showwarning("Error", "Please check Roll No.!\n Entered roll number already present !",
                                parent=Frame_right)
                        else:
                            value = tmg.askquestion("Add", "Do you want to add " + str(name_entrybox.get()) + " in " + roman_classno + " - " + str(section_selS.get()) + " ?")
                            if (value == 'yes'):
                                if (class_no > 10):
                                    st = 1
                                    c.execute("UPDATE USER set ST = :st WHERE USER_ID = :name",
                                              {'name': str(user_data[0]), 'st': 1})
                                    c.execute("INSERT INTO SENIOR(USER_NAME, USER_CLASS, USER_STREAM, USER_ROLL, DOB_DATE, DOB_MONTH, DOB_YEAR, GENDER, GUARDIAN_NAME, ADDRESS, OPTIONAL, BENGALI_UNIT, BENGALI_HALF, BENGALI_FINAL, ENGLISH_UNIT, ENGLISH_HALF, ENGLISH_FINAL, HISTORY_UNIT, HISTORY_HALF, HISTORY_FINAL, PHILOSOPHY_UNIT, PHILOSOPHY_HALF, PHILOSOPHY_FINAL, GEOGRAPHY_UNIT, GEOGRAPHY_HALF, GEOGRAPHY_FINAL, EDUCATION_UNIT, EDUCATION_HALF, EDUCATION_FINAL, POLITICAL_UNIT, POLITICAL_HALF, POLITICAL_FINAL, BUSINESS_UNIT, BUSINESS_HALF, BUSINESS_FINAL, ECONOMICS_UNIT, ECONOMICS_HALF, ECONOMICS_FINAL, ACCOUNT_UNIT, ACCOUNT_HALF, ACCOUNT_FINAL, LAW_UNIT, LAW_HALF, LAW_FINAL, COMA_UNIT, COMA_HALF, COMA_FINAL, PHYSICS_UNIT, PHYSICS_HALF, PHYSICS_FINAL, CHEMISTRY_UNIT, CHEMISTRY_HALF, CHEMISTRY_FINAL, MATH_UNIT, MATH_HALF, MATH_FINAL, BIOLOGY_UNIT, BIOLOGY_HALF, BIOLOGY_FINAL, COMS_UNIT, COMS_HALF, COMS_FINAL) \
                                                                        VALUES (:name, :class, :stream, :roll, :ddate, :dmonth, :dyear, :gender, :gname, :address, :optional, :benu, :benh, :benf, :engu, :engh, :engf, :hisu, :hish, :hisf, :phiu, :phih, :phif, :geou, :geoh, :geof, :eduu, :eduh, :eduf, :polu, :polh, :polf, :busu, :bush, :busf, :ecou, :ecoh, :ecof, :accu, :acch, :accf, :lawu, :lawh, :lawf, :comau, :comah, :comaf, :physu, :physh, :physf, :chemu, :chemh, :chemf, :mathu, :mathh, :mathf, :biou, :bioh, :biof, :comsu, :comsh, :comsf)",
                                              {'name': name_entrybox.get(), 'class': str(class_no),
                                               'stream': section_selS.get(),
                                               'roll': roll_entry.get(), 'ddate': str(dob_dateS.get()),
                                               'dmonth': str(dob_monthS.get()), 'dyear': str(dob_yearS.get()),
                                               'gender': genderS.get(),
                                               'gname': guardian_name_entrybox.get(),
                                               'address': adress_textboxT.get(1.0, END),
                                               'optional': select_optional_subS.get(), 'benu': 0, 'benh': 0, 'benf': 0,
                                               'engu': 0, 'engh': 0, 'engf': 0,
                                               'hisu': 0, 'hish': 0, 'hisf': 0, 'phiu': 0, 'phih': 0, 'phif': 0,
                                               'geou': 0, 'geoh': 0, 'geof': 0, 'eduu': 0, 'eduh': 0, 'eduf': 0,
                                               'polu': 0, 'polh': 0, 'polf': 0,
                                               'busu': 0, 'bush': 0, 'busf': 0, 'ecou': 0, 'ecoh': 0, 'ecof': 0,
                                               'accu': 0, 'acch': 0, 'accf': 0, 'lawu': 0, 'lawh': 0, 'lawf': 0,
                                               'comau': 0, 'comah': 0, 'comaf': 0,
                                               'physu': 0, 'physh': 0, 'physf': 0, 'chemu': 0, 'chemh': 0, 'chemf': 0,
                                               'mathu': 0, 'mathh': 0, 'mathf': 0, 'biou': 0, 'bioh': 0, 'biof': 0,
                                               'comsu': 0, 'comsh': 0, 'comsf': 0})
                                    conn.commit()
                                    data_entry()

                                elif ((class_no >= 5) and (class_no <= 10)):
                                    mt = 1
                                    c.execute("UPDATE USER set MT = :mt WHERE USER_ID = :name",
                                              {'name': str(user_data[0]), 'mt': 1})
                                    c.execute("INSERT INTO MIDDLE(USER_NAME, USER_CLASS, USER_SEC, USER_ROLL, DOB_DATE, DOB_MONTH, DOB_YEAR, GENDER, GUARDIAN_NAME, ADDRESS, BENGALI_UNIT, BENGALI_HALF, BENGALI_FINAL, ENGLISH_UNIT, ENGLISH_HALF, ENGLISH_FINAL, MATH_UNIT, MATH_HALF, MATH_FINAL, HISTORY_UNIT, HISTORY_HALF, HISTORY_FINAL, GEOGRAPHY_UNIT, GEOGRAPHY_HALF, GEOGRAPHY_FINAL, PHYS_UNIT, PHYS_HALF, PHYS_FINAL, LIFE_UNIT, LIFE_HALF, LIFE_FINAL) \
                                                                        VALUES (:name, :class, :sec, :roll, :ddate, :dmonth, :dyear, :gender, :gname, :address, :benu, :benh, :benf, :engu, :engh, :engf, :mathu, :mathh, :mathf, :hisu, :hish, :hisf, :geou, :geoh, :geof, :phyu, :phyh, :phyf, :lifu, :lifh, :liff)",
                                              {'name': name_entrybox.get(), 'class': str(class_no),
                                               'sec': section_selS.get(), 'roll': roll_entry.get(),
                                               'ddate': str(dob_dateS.get()), 'dmonth': str(dob_monthS.get()),
                                               'dyear': str(dob_yearS.get()), 'gender': genderS.get(),
                                               'gname': guardian_name_entrybox.get(),
                                               'address': adress_textboxT.get(1.0, END), 'benu': 0, 'benh': 0,
                                               'benf': 0, 'engu': 0, 'engh': 0, 'engf': 0, 'mathu': 0, 'mathh': 0,
                                               'mathf': 0, 'hisu': 0, 'hish': 0, 'hisf': 0, 'geou': 0, 'geoh': 0,
                                               'geof': 0, 'phyu': 0, 'phyh': 0, 'phyf': 0, 'lifu': 0, 'lifh': 0,
                                               'liff': 0})
                                    conn.commit()
                                    data_entry()
                                else:
                                    jt = 1
                                    c.execute("UPDATE USER set JT = :jt WHERE USER_ID = :name",
                                              {'name': str(user_data[0]), 'jt': 1})
                                    c.execute("INSERT INTO JUNIOR(USER_NAME, USER_CLASS, USER_SEC, USER_ROLL, DOB_DATE, DOB_MONTH, DOB_YEAR, GENDER, GUARDIAN_NAME, ADDRESS, BENGALI_UNIT, BENGALI_HALF, BENGALI_FINAL, ENGLISH_UNIT, ENGLISH_HALF, ENGLISH_FINAL, MATH_UNIT, MATH_HALF, MATH_FINAL, GK_UNIT, GK_HALF, GK_FINAL) \
                                                                        VALUES (:name, :class, :sec, :roll, :ddate, :dmonth, :dyear, :gender, :gname, :address, :benu, :benh, :benf, :engu, :engh, :engf, :mathu, :mathh, :mathf, :gku, :gkh, :gkf)",
                                              {'name': name_entrybox.get(), 'class': str(class_no),
                                               'sec': section_selS.get(), 'roll': roll_entry.get(),
                                               'ddate': str(dob_dateS.get()), 'dmonth': str(dob_monthS.get()),
                                               'dyear': str(dob_yearS.get()), 'gender': genderS.get(),
                                               'gname': guardian_name_entrybox.get(),
                                               'address': adress_textboxT.get(1.0, END), 'benu': 0, 'benh': 0,
                                               'benf': 0, 'engu': 0, 'engh': 0, 'engf': 0, 'mathu': 0, 'mathh': 0,
                                               'mathf': 0, 'gku': 0, 'gkh': 0, 'gkf': 0})
                                    conn.commit()
                                    data_entry()

            global Frame_right
            Frame_right.destroy()
            Frame_right = Frame(root)
            Frame_right.place(x=350, y=60, height=600, width=900)

            studentnameS = StringVar()
            section_selS = StringVar()
            rollS = StringVar()
            dob_dateS = StringVar()
            dob_monthS = StringVar()
            dob_yearS = StringVar()
            guardian_nameS = StringVar()
            genderS = StringVar()

            enter_details_label = Label(Frame_right, text="Enter Student Details to ADD", font=("Goudy old style", 25, "bold"),fg="black")
            name_label= Label(Frame_right, text="Name", font=("Goudy old style", 15, "bold"), fg="black")
            name_entrybox= Entry(Frame_right, textvariable=studentnameS, font=("times new roman", 15), bg="light grey")
            class_label= Label(Frame_right, text="Class", font=("Goudy old style", 15, "bold"), fg="black")
            class_roman_label= Label(Frame_right, text=str(roman_classno), font=("Goudy old style", 15, "bold"), fg="black")
            section_label= Label(Frame_right, text="Section", font=("Goudy old style", 15, "bold"), fg="black")

            name_label.place(x=90, y=90)
            enter_details_label.place(x=250, y=20)
            name_entrybox.place(x=250, y=90, width=350, height=30)
            class_label.place(x=90, y=130)
            class_roman_label.place(x=250, y=130)

            select_secD= ttk.Combobox(Frame_right,textvariable=section_selS,font=(15),state= "readonly")
            if (class_no < 5):
                section_label.configure(text="Section")
                select_secD.configure(value=["A", "B", "C"])
                select_secD.current(0)

                section_label.place(x=320, y=130)
                select_secD.place(x=390, y=130, width=100, height=30)

                c.execute("UPDATE USER set JT = :jt WHERE USER_ID = :name",{'name': str(user_data[0]), 'jt': 1})
                c.execute("SELECT JT FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                d = c.fetchall()
                roll = []
                if (d[0][0] == 1):
                    c.execute("SELECT * FROM JUNIOR")
                    data = c.fetchall()
                    for record in data:
                        roll.append(record[3])

            elif (class_no >= 5 and class_no <= 10):
                section_label.configure(text="Section")
                select_secD.configure(value=["A", "B", "C"])
                select_secD.current(0)

                section_label.place(x=320, y=130)
                select_secD.place(x=390, y=130, width=100, height=30)

                c.execute("UPDATE USER set MT = :mt WHERE USER_ID = :name",{'name': str(user_data[0]), 'mt': 1})
                c.execute("SELECT MT FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                d = c.fetchall()
                if (d[0][0] == 1):
                    c.execute("SELECT * FROM MIDDLE")
                    data = c.fetchall()
                    roll = []
                    for record in data:
                        roll.append(record[3])

            elif (class_no > 10):
                def comboclickoptsub(event):
                    if(select_secD.get()=="Arts"):
                        select_optional_subD.configure(value=["Education", "Political Science"])
                    elif(select_secD.get()== "Commerce"):
                        select_optional_subD.configure(value=["Law and Audit", "Computer Application"])
                    elif(select_secD.get()== "Science"):
                        select_optional_subD.configure(value=["Biology", "Computer Science"])
                    select_optional_subD.current(0)

                select_optional_subS = StringVar()
                section_label.configure(text="Stream")
                select_secD.configure(value=["Arts", "Commerce", "Science"])
                select_secD.current(0)
                select_optional_sub_label = Label(Frame_right, text="Optional Subject",font=("Goudy old style", 15, "bold"), fg="black")
                select_optional_subD = ttk.Combobox(Frame_right, textvariable=select_optional_subS, font=(15),state="readonly")

                section_label.place(x=300, y=130)
                select_secD.place(x=390, y=130, width=100, height=30)
                select_optional_sub_label.place(x=520, y=130)
                select_optional_subD.place(x=680,y=130,width=170, height=30)

                if (select_secD.get() == "Arts"):
                    select_optional_subD.configure(value=["Education", "Political Science"])
                    select_optional_subD.current(0)

                select_secD.bind("<<ComboboxSelected>>", comboclickoptsub)

                c.execute("UPDATE USER set ST = :st WHERE USER_ID = :name",{'name': str(user_data[0]), 'st': 1})
                c.execute("SELECT ST FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                d = c.fetchall()
                if (d[0][0] == 1):
                    c.execute("SELECT * FROM SENIOR")
                    data = c.fetchall()
                    roll = []
                    for record in data:
                        roll.append(record[3])

            roll_label= Label(Frame_right, text="Roll No.", font=("Goudy old style", 15, "bold"), fg="black")
            roll_entry = Entry(Frame_right, textvariable=rollS, font=("times new roman", 15), bg="light grey")
            dob_label= Label(Frame_right, text="Date of Birth", font=("Goudy old style", 15, "bold"), fg="black" )
            dob_dateD =ttk.Combobox(Frame_right,textvariable=dob_dateS,font=(15),value=[x for x in range(1,32)],state="readonly")
            dob_monthD = ttk.Combobox(Frame_right,textvariable=dob_monthS,font=(15),value=[y for y in range(1,13)],state="readonly")
            slash1_label = Label(Frame_right, text="/", font=("Goudy old style", 15, "bold"),fg="black")
            slash2_label = Label(Frame_right, text="/", font=("Goudy old style", 15, "bold"),fg="black")
            dob_yearD = ttk.Combobox(Frame_right,textvariable=dob_yearS,font=(15),value=[z for z in range(2020,1980,-1)],state="readonly")
            gender_label = Label(Frame_right, text="Gender", font=("Goudy old style", 15, "bold"), fg="black")
            select_genderD= ttk.Combobox(Frame_right,textvariable=genderS,font=(15),value=["Male","Female"],state="readonly")
            guardian_name_label= Label(Frame_right, text="Guardian's Name", font=("Goudy old style", 15, "bold"), fg="black")
            guardian_name_entrybox= Entry(Frame_right, textvariable=guardian_nameS, font=("times new roman", 15), bg="light grey")
            address_label= Label(Frame_right, text="Address", font=("Goudy old style", 15, "bold"), fg="black")
            adress_textboxT = ScrolledText(Frame_right,width=55,height=9,font=("times new roman", 15), bg="light grey")
            entryadd_button= Button(Frame_right,command=entry_add, text="Add", fg="black", bg="sky blue", font=("times new roman", 15))

            roll_label.place(x=90, y=170)
            roll_entry.place(x=250, y=170, width=350, height=30)
            dob_label.place(x=90, y=210)
            dob_dateD.place(x=250, y=210, width=50, height=30)
            slash1_label.place(x=315, y=210)
            dob_monthD.place(x=340, y=210, width=50, height=30)
            slash2_label.place(x=400, y=210)
            dob_yearD.place(x=430, y=210, width=90, height=30)
            gender_label.place(x=90, y=250)
            select_genderD.place(x=250, y=250, width=90, height=30)
            guardian_name_label.place(x=90, y=290)
            guardian_name_entrybox.place(x=250, y=290, width=350, height=30)
            address_label.place(x=90, y=350)
            adress_textboxT.place(x=250, y=350)
            entryadd_button.place(x=650, y=210,height=50, width=100)

        global Frame_right
        Frame_right.destroy()
        Frame_right = Frame(root)
        Frame_right.place(x=350, y=60, height=600, width=900)
        FR_BG = Label(Frame_right, image=bg4)
        FR_BG.place(x=0, y=0, relwidth=1, relheight=1)
        select_class_label = Label(Frame_right,text="Select Class to Add Students",font=("Goudy old style", 25, "bold"),bg="white", fg="black")
        select_class_label.place(x=250, y=40)

        class1_button= Button(Frame_right,command=lambda:entry_class(1,"I"), text="Class I", fg="black",bg="sky blue", font=("times new roman", 15))
        class2_button = Button(Frame_right, command=lambda:entry_class(2,"II"), text="Class II", fg="black",bg="sky blue", font=("times new roman", 15))
        class3_button= Button(Frame_right, command=lambda: entry_class(3,"III"), text="Class III", fg="black",bg="sky blue", font=("times new roman", 15))
        class4_button = Button(Frame_right, command=lambda: entry_class(4,"IV"), text="Class IV", fg="black",bg="sky blue", font=("times new roman", 15))
        class5_button = Button(Frame_right, command=lambda: entry_class(5,"V"), text="Class V", fg="black",bg="sky blue", font=("times new roman", 15))
        class6_button = Button(Frame_right, command=lambda: entry_class(6,"VI"), text="Class VI", fg="black",bg="sky blue", font=("times new roman", 15))
        class7_button = Button(Frame_right, command=lambda: entry_class(7,"VII"), text="Class VII", fg="black",bg="sky blue", font=("times new roman", 15))
        class8_button = Button(Frame_right, command=lambda: entry_class(8,"VIII"), text="Class VIII", fg="black",bg="sky blue", font=("times new roman", 15))
        class9_button = Button(Frame_right, command=lambda: entry_class(9,"IX"), text="Class IX", fg="black",bg="sky blue", font=("times new roman", 15))
        class10_button = Button(Frame_right, command=lambda: entry_class(10,"X"), text="Class X", fg="black",bg="sky blue", font=("times new roman", 15))
        class11_button = Button(Frame_right, command=lambda: entry_class(11,"XI"), text="Class XI", fg="black",bg="sky blue", font=("times new roman", 15))
        class12_button = Button(Frame_right, command=lambda: entry_class(12,"XII"), text="Class XII", fg="black",bg="sky blue", font=("times new roman", 15))

        class1_button.place(x=180, y=110, height=40, width=100)
        class2_button.place(x=400, y=110, height=40, width=100)
        class3_button.place(x=620, y=110, height=40, width=100)
        class4_button.place(x=180, y=220, height=40, width=100)
        class5_button.place(x=400, y=220, height=40, width=100)
        class6_button.place(x=620, y=220, height=40, width=100)
        class7_button.place(x=180, y=330, height=40, width=100)
        class8_button.place(x=400, y=330, height=40, width=100)
        class9_button.place(x=620, y=330, height=40, width=100)
        class10_button.place(x=180, y=440, height=40, width=100)
        class11_button.place(x=400, y=440, height=40, width=100)
        class12_button.place(x=620, y=440, height=40, width=100)

    def marks_entry():

        def comboclick1(event):
            if(sel_secD.get()=="" and sel_subD.get()==""):
                selected_lbl.configure(text="Selected " + str(sel_classD.get()) + " ➖ Section None ➖ Subject None")
            if(sel_classD.get() in ["XI","XII"]):
                sel_secD.configure(value=["Arts", "Commerce", "Science"])
                sel_secD.current(0)
                if (sel_secD.get() == "Arts"):
                    sel_subD.configure(values=["Bengali", "English","History", "Philosophy", "Geography","Education", "Political Science"])
                    sel_subD.current(0)
                selected_lbl.configure(text="Selected " + str(sel_classD.get()) + " ➖ Stream " + str(sel_secD.get())+"➖ Subject "+ str(sel_subD.get()))
                section_label.configure(text="Stream")
            elif(sel_classD.get()!="XI" or sel_classD.get()!="XII"):
                sel_secD.configure(value=["A", "B", "C"])
                sel_secD.current(0)
                if (sel_classD.get() in ["V", "VI", "VII", "VIII", "IX", "X"]):
                    sel_subD.configure(values=["Bengali", "English", "Mathematics", "History", "Geography", "Physical Science","Life Science"])
                    sel_subD.current(0)
                if (sel_classD.get() in ["I", "II", "III", "IV"]):
                    sel_subD.configure(values=["Bengali", "English", "Mathematics", "GK"])
                    sel_subD.current(0)
                selected_lbl.configure(text="Selected " + str(sel_classD.get()) + " ➖ Section " + str(sel_secD.get()) + "➖ Subject " + str(sel_subD.get()))
                section_label.configure(text="Section")

        def comboclick2(event):
            if (sel_classD.get() == "" and sel_subD.get()==""):
                selected_lbl.configure(text="Selected Class None ➖ Section " + str(sel_secD.get())+"➖ Subject None")
            if (sel_classD.get() in ["XI","XII"]):
                if(sel_secD.get()=="Science"):
                    sel_subD.configure(values=["Bengali", "English","Physics", "Chemistry", "Mathematics","Biology", "Computer Science"])
                    sel_subD.current(0)
                if(sel_secD.get()=="Commerce"):
                    sel_subD.configure(values=["Bengali", "English", "Business Studies","Economics", "Accountancy","Law and Audit", "Computer Application"])
                    sel_subD.current(0)
                if (sel_secD.get() == "Arts"):
                    sel_subD.configure(values=["Bengali", "English","History", "Philosophy", "Geography","Education", "Political Science"])
                    sel_subD.current(0)
                selected_lbl.configure(text="Selected " + str(sel_classD.get()) + " ➖ Stream " + str(sel_secD.get())+"➖ Subject "+ str(sel_subD.get()))
                section_label.configure(text="Stream")
            elif(sel_classD.get() in ["V","VI","VII","VIII","IX","X"]):
                sel_subD.configure(values=["Bengali", "English","Mathematics","History", "Geography", "Physical Science", "Life Science"])
                sel_subD.current(0)
                selected_lbl.configure(text="Selected " + str(sel_classD.get()) + " ➖ Section " + str(sel_secD.get())+"➖ Subject "+ str(sel_subD.get()))
                section_label.configure(text="Section")
            elif(sel_classD.get() in ["I","II","III","IV"]):
                sel_subD.configure(values=["Bengali", "English", "Mathematics", "GK"])
                sel_subD.current(0)
                selected_lbl.configure(text="Selected " + str(sel_classD.get()) + " ➖ Section " + str(sel_secD.get()) + "➖ Subject "+ str(sel_subD.get()))
                section_label.configure(text="Section")

        def comboclick3(event):
            if (sel_classD.get() == "" and sel_secD.get()==""):
                selected_lbl.configure(text="Selected Class None ➖ Section None ➖ Subject " + str(sel_subD.get()))
            else:
                if (sel_classD.get() in ["XI", "XII"]):
                    selected_lbl.configure(text="Selected " + str(sel_classD.get()) + " ➖ Stream " + str(sel_secD.get()) + "➖ Subject " + str(sel_subD.get()))
                elif (sel_classD.get() != "XI" or sel_classD.get() != "XII"):
                    selected_lbl.configure(text="Selected " + str(sel_classD.get()) + " ➖ Section " + str(sel_secD.get()) + "➖ Subject " + str(sel_subD.get()))

        def go():
            def add_marks(option):
                def add(opt,marks):
                    if (opt == 1):
                        if(class_roman_to_numerical[sel_classS.get()]== 11 or class_roman_to_numerical[sel_classS.get()]== 12):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE SENIOR set BENGALI_UNIT = :benu WHERE USER_ROLL = :roll",
                                          {'benu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE SENIOR set ENGLISH_UNIT = :engu WHERE USER_ROLL = :roll",
                                          {'engu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE SENIOR set HISTORY_UNIT = :hisu WHERE USER_ROLL = :roll",
                                          {'hisu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Philosophy"):
                                c.execute("UPDATE SENIOR set PHILOSOPHY_UNIT = :phiu WHERE USER_ROLL = :roll",
                                          {'phiu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE SENIOR set GEOGRAPHY_UNIT = :geou WHERE USER_ROLL = :roll",
                                          {'geou': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Education"):
                                c.execute("UPDATE SENIOR set EDUCATION_UNIT = :eduu WHERE USER_ROLL = :roll",
                                          {'eduu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Political Science"):
                                c.execute("UPDATE SENIOR set POLITICAL_UNIT = :polu WHERE USER_ROLL = :roll",
                                          {'polu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Business Studies"):
                                c.execute("UPDATE SENIOR set BUSINESS_UNIT = :busu WHERE USER_ROLL = :roll",
                                          {'busu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Economics"):
                                c.execute("UPDATE SENIOR set ECONOMICS_UNIT = :ecou WHERE USER_ROLL = :roll",
                                          {'ecou': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Accountancy"):
                                c.execute("UPDATE SENIOR set ACCOUNT_UNIT = :accu WHERE USER_ROLL = :roll",
                                          {'accu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Law and Audit"):
                                c.execute("UPDATE SENIOR set LAW_UNIT = :lawu WHERE USER_ROLL = :roll",
                                          {'lawu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Application"):
                                c.execute("UPDATE SENIOR set COMA_UNIT = :comau WHERE USER_ROLL = :roll",
                                          {'comau': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physics"):
                                c.execute("UPDATE SENIOR set PHYSICS_UNIT = :physu WHERE USER_ROLL = :roll",
                                          {'physu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Chemistry"):
                                c.execute("UPDATE SENIOR set CHEMISTRY_UNIT = :chemu WHERE USER_ROLL = :roll",
                                          {'chemu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE SENIOR set MATH_UNIT = :mathu WHERE USER_ROLL = :roll",
                                          {'mathu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Biology"):
                                c.execute("UPDATE SENIOR set BIOLOGY_UNIT = :biou WHERE USER_ROLL = :roll",
                                          {'biou': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Science"):
                                c.execute("UPDATE SENIOR set COMS_UNIT = :comsu WHERE USER_ROLL = :roll",
                                          {'comsu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()

                        elif (class_roman_to_numerical[sel_classS.get()] >= 5 and class_roman_to_numerical[sel_classS.get()] <= 10):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE MIDDLE set BENGALI_UNIT = :benu WHERE USER_ROLL = :roll",
                                          {'benu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE MIDDLE set ENGLISH_UNIT = :engu WHERE USER_ROLL = :roll",
                                          {'engu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE MIDDLE set MATH_UNIT = :mathu WHERE USER_ROLL = :roll",
                                          {'mathu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE MIDDLE set HISTORY_UNIT = :hisu WHERE USER_ROLL = :roll",
                                          {'hisu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE MIDDLE set GEOGRAPHY_UNIT = :geou WHERE USER_ROLL = :roll",
                                          {'geou': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physical Science"):
                                c.execute("UPDATE MIDDLE set PHYS_UNIT = :phyu WHERE USER_ROLL = :roll",
                                          {'phyu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Life Science"):
                                c.execute("UPDATE MIDDLE set LIFE_UNIT = :lifu WHERE USER_ROLL = :roll",
                                          {'lifu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()

                        elif (class_roman_to_numerical[sel_classS.get()] < 5):
                            if(str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE JUNIOR set BENGALI_UNIT = :benu WHERE USER_ROLL = :roll",
                                    {'benu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif(str(sel_subD.get()) == "English"):
                                c.execute("UPDATE JUNIOR set ENGLISH_UNIT = :engu WHERE USER_ROLL = :roll",
                                          {'engu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif(str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE JUNIOR set MATH_UNIT = :mathu WHERE USER_ROLL = :roll",
                                          {'mathu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif(str(sel_subD.get()) == "GK"):
                                c.execute("UPDATE JUNIOR set GK_UNIT = :gku WHERE USER_ROLL = :roll",
                                          {'gku': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                    elif (opt == 2):
                        if(class_roman_to_numerical[sel_classS.get()]== 11 or class_roman_to_numerical[sel_classS.get()]== 12):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE SENIOR set BENGALI_HALF = :benh WHERE USER_ROLL = :roll",
                                          {'benh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE SENIOR set ENGLISH_HALF = :engh WHERE USER_ROLL = :roll",
                                          {'engh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE SENIOR set HISTORY_HALF = :hish WHERE USER_ROLL = :roll",
                                          {'hish': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Philosophy"):
                                c.execute("UPDATE SENIOR set PHILOSOPHY_HALF = :phih WHERE USER_ROLL = :roll",
                                          {'phih': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE SENIOR set GEOGRAPHY_HALF = :geoh WHERE USER_ROLL = :roll",
                                          {'geoh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Education"):
                                c.execute("UPDATE SENIOR set EDUCATION_HALF = :eduh WHERE USER_ROLL = :roll",
                                          {'eduh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Political Science"):
                                c.execute("UPDATE SENIOR set POLITICAL_HALF = :polh WHERE USER_ROLL = :roll",
                                          {'polh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Business Studies"):
                                c.execute("UPDATE SENIOR set BUSINESS_HALF = :bush WHERE USER_ROLL = :roll",
                                          {'bush': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Economics"):
                                c.execute("UPDATE SENIOR set ECONOMICS_HALF = :ecoh WHERE USER_ROLL = :roll",
                                          {'ecoh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Accountancy"):
                                c.execute("UPDATE SENIOR set ACCOUNT_HALF = :acch WHERE USER_ROLL = :roll",
                                          {'acch': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Law and Audit"):
                                c.execute("UPDATE SENIOR set LAW_HALF = :lawh WHERE USER_ROLL = :roll",
                                          {'lawh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Application"):
                                c.execute("UPDATE SENIOR set COMA_HALF = :comah WHERE USER_ROLL = :roll",
                                          {'comah': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physics"):
                                c.execute("UPDATE SENIOR set PHYSICS_HALF = :physh WHERE USER_ROLL = :roll",
                                          {'physh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Chemistry"):
                                c.execute("UPDATE SENIOR set CHEMISTRY_HALF = :chemh WHERE USER_ROLL = :roll",
                                          {'chemh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE SENIOR set MATH_HALF = :mathh WHERE USER_ROLL = :roll",
                                          {'mathh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Biology"):
                                c.execute("UPDATE SENIOR set BIOLOGY_HALF = :bioh WHERE USER_ROLL = :roll",
                                          {'bioh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Science"):
                                c.execute("UPDATE SENIOR set COMS_HALF = :comsh WHERE USER_ROLL = :roll",
                                          {'comsh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                        elif (class_roman_to_numerical[sel_classS.get()] >= 5 and class_roman_to_numerical[sel_classS.get()] <= 10):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE MIDDLE set BENGALI_HALF = :benh WHERE USER_ROLL = :roll",
                                          {'benh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE MIDDLE set ENGLISH_HALF = :engh WHERE USER_ROLL = :roll",
                                          {'engh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE MIDDLE set MATH_HALF = :mathh WHERE USER_ROLL = :roll",
                                          {'mathh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE MIDDLE set HISTORY_HALF = :hish WHERE USER_ROLL = :roll",
                                          {'hish': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE MIDDLE set GEOGRAPHY_HALF = :geoh WHERE USER_ROLL = :roll",
                                          {'geoh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physical Science"):
                                c.execute("UPDATE MIDDLE set PHYS_HALF = :phyh WHERE USER_ROLL = :roll",
                                          {'phyh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Life Science"):
                                c.execute("UPDATE MIDDLE set LIFE_HALF = :lifh WHERE USER_ROLL = :roll",
                                          {'lifh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()

                        elif(class_roman_to_numerical[sel_classS.get()] < 5):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE JUNIOR set BENGALI_HALF = :benh WHERE USER_ROLL = :roll",
                                        {'benh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE JUNIOR set ENGLISH_HALF = :engh WHERE USER_ROLL = :roll", {'engh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE JUNIOR set MATH_HALF = :mathh WHERE USER_ROLL = :roll", {'mathh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "GK"):
                                c.execute("UPDATE JUNIOR set GK_HALF = :gkh WHERE USER_ROLL = :roll", {'gkh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                    elif (opt == 3):
                        if (class_roman_to_numerical[sel_classS.get()] == 11 or class_roman_to_numerical[sel_classS.get()] == 12):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE SENIOR set BENGALI_FINAL = :benf WHERE USER_ROLL = :roll",
                                          {'benf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE SENIOR set ENGLISH_FINAL = :engf WHERE USER_ROLL = :roll",
                                          {'engf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE SENIOR set HISTORY_FINAL = :hisf WHERE USER_ROLL = :roll",
                                          {'hisf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Philosophy"):
                                c.execute("UPDATE SENIOR set PHILOSOPHY_FINAL = :phif WHERE USER_ROLL = :roll",
                                          {'phif': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE SENIOR set GEOGRAPHY_FINAL = :geof WHERE USER_ROLL = :roll",
                                          {'geof': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Education"):
                                c.execute("UPDATE SENIOR set EDUCATION_FINAL = :eduf WHERE USER_ROLL = :roll",
                                          {'eduf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Political Science"):
                                c.execute("UPDATE SENIOR set POLITICAL_FINAL = :polf WHERE USER_ROLL = :roll",
                                          {'polf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Business Studies"):
                                c.execute("UPDATE SENIOR set BUSINESS_FINAL = :busf WHERE USER_ROLL = :roll",
                                          {'busf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Economics"):
                                c.execute("UPDATE SENIOR set ECONOMICS_FINAL = :ecof WHERE USER_ROLL = :roll",
                                          {'ecof': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Accountancy"):
                                c.execute("UPDATE SENIOR set ACCOUNT_FINAL = :accf WHERE USER_ROLL = :roll",
                                          {'accf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Law and Audit"):
                                c.execute("UPDATE SENIOR set LAW_FINAL = :lawf WHERE USER_ROLL = :roll",
                                          {'lawf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Application"):
                                c.execute("UPDATE SENIOR set COMA_FINAL = :comaf WHERE USER_ROLL = :roll",
                                          {'comaf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physics"):
                                c.execute("UPDATE SENIOR set PHYSICS_FINAL = :physf WHERE USER_ROLL = :roll",
                                          {'physf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Chemistry"):
                                c.execute("UPDATE SENIOR set CHEMISTRY_FINAL = :chemf WHERE USER_ROLL = :roll",
                                          {'chemf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE SENIOR set MATH_FINAL = :mathf WHERE USER_ROLL = :roll",
                                          {'mathf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Biology"):
                                c.execute("UPDATE SENIOR set BIOLOGY_FINAL = :biof WHERE USER_ROLL = :roll",
                                          {'biof': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Science"):
                                c.execute("UPDATE SENIOR set COMS_FINAL = :comsf WHERE USER_ROLL = :roll",
                                          {'comsf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                        elif (class_roman_to_numerical[sel_classS.get()] >= 5 and class_roman_to_numerical[sel_classS.get()] <= 10):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE MIDDLE set BENGALI_FINAL = :benf WHERE USER_ROLL = :roll",
                                          {'benf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE MIDDLE set ENGLISH_FINAL = :engf WHERE USER_ROLL = :roll",
                                          {'engf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE MIDDLE set MATH_FINAL = :mathf WHERE USER_ROLL = :roll",
                                          {'mathf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE MIDDLE set HISTORY_FINAL = :hisf WHERE USER_ROLL = :roll",
                                          {'hisf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE MIDDLE set GEOGRAPHY_FINAL = :geof WHERE USER_ROLL = :roll",
                                          {'geof': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physical Science"):
                                c.execute("UPDATE MIDDLE set PHYS_FINAL = :phyf WHERE USER_ROLL = :roll",
                                          {'phyf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Life Science"):
                                c.execute("UPDATE MIDDLE set LIFE_FINAL = :liff WHERE USER_ROLL = :roll",
                                          {'liff': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                        elif (class_roman_to_numerical[sel_classS.get()] < 5):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE JUNIOR set BENGALI_FINAL = :benf WHERE USER_ROLL = :roll",{'benf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE JUNIOR set ENGLISH_FINAL = :engf WHERE USER_ROLL = :roll", {'engf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE JUNIOR set MATH_FINAL = :mathf WHERE USER_ROLL = :roll", {'mathf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "GK"):
                                c.execute("UPDATE JUNIOR set GK_FINAL = :gkf WHERE USER_ROLL = :roll", {'gkf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                    add_marks_top.destroy()

                sel_row = marksentry_tree.selection()
                if (len(sel_row) > 1):
                    tmg.showwarning("Error", "Please select One Student !", parent=Frame_right)
                elif (len(sel_row) == 0):
                    tmg.showwarning("Error", "Please select One Student to add marks !", parent=Frame_right)
                else:
                    user_sel = marksentry_tree.item(sel_row, 'values')
                    add_marks_top = Toplevel(Frame_right)
                    add_marks_top.title("Add Marks")
                    add_marks_top.geometry("550x290+0+0")
                    add_marks_top.resizable(False, False)
                    TOP_BG = Label(add_marks_top, image=bgtop3)
                    TOP_BG.place(x=0, y=0, relwidth=1, relheight=1)

                    marksS = StringVar()
                    marksS.set("0")
                    name_lbl = Label(add_marks_top, text="Name",font=("Goudy old style", 15, "bold"), fg="black").place(x=20,y=20)
                    nameE_lbl= Label(add_marks_top,text=str(user_sel[1]),font=("Goudy old style", 15, "bold"), fg="black").place(x=250,y=20)
                    class_lbl= Label(add_marks_top,text="Class",font=("Goudy old style", 15, "bold"), fg="black").place(x=20,y=50)
                    classE_lbl = Label(add_marks_top,text=str(class_roman_to_numerical[sel_classS.get()]),font=("Goudy old style", 15, "bold"), fg="black").place(x=250,y=50)
                    secE_lbl = Label(add_marks_top,text=str(sel_secD.get()),font=("Goudy old style", 15, "bold"), fg="black").place(x=250,y=80)
                    roll_label = Label(add_marks_top,text="Roll No",font=("Goudy old style", 15, "bold"), fg="black").place(x=20,y=110)
                    rollE_lbl = Label(add_marks_top, text=str(user_sel[0]),font=("Goudy old style", 15, "bold"), fg="black").place(x=250,y=110)
                    subject_lbl = Label(add_marks_top, text="Subject", font=("Goudy old style", 15, "bold"),fg="black").place(x=20,y=140)
                    subjectE_lbl =Label(add_marks_top,text=str(sel_subD.get()),font=("Goudy old style", 15, "bold"), fg="black").place(x=250,y=140)
                    entermarksE= Entry(add_marks_top, textvariable=marksS, font=("times new roman", 15), bg="light grey")
                    entermarksE.place(x=250, y=170, width=100, height=30)
                    add_button = Button(add_marks_top, command=lambda: add(option,str(marksS.get())), text="Add", fg="black", bg="sky blue",
                                     font=("times new roman", 15))
                    add_button.place(x=80, y=220, height=30, width=80)
                    cancel_button = Button(add_marks_top, command=add_marks_top.destroy, text="Cancel", fg="black",bg="sky blue", font=("times new roman", 15))
                    cancel_button.place(x=250, y=220, height=30, width=80)
                    if (option == 1):
                        if(class_roman_to_numerical[sel_classS.get()]== 11 or class_roman_to_numerical[sel_classS.get()]== 12):
                            section_label = Label(add_marks_top,text="Stream", font=("Goudy old style", 15, "bold"), fg="black").place(x=20,y=80)
                        elif(class_roman_to_numerical[sel_classS.get()]!= 11 or class_roman_to_numerical[sel_classS.get()]!= 12):
                            section_label = Label(add_marks_top, text="Section", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=80)
                        entermarks_lbl = Label(add_marks_top,text="Enter Unit Marks", font=("Goudy old style", 15, "bold"), fg="black").place(x=20, y=170)
                    elif (option == 2):
                        if(class_roman_to_numerical[sel_classS.get()]== 11 or class_roman_to_numerical[sel_classS.get()]== 12):
                            section_label = Label(add_marks_top,text="Stream", font=("Goudy old style", 15, "bold"), fg="black").place(x=20,y=80)
                        elif(class_roman_to_numerical[sel_classS.get()]!= 11 or class_roman_to_numerical[sel_classS.get()]!= 12):
                            section_label = Label(add_marks_top, text="Section", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=80)
                        entermarks_lbl = Label(add_marks_top,text="Enter Half Yearly Marks", font=("Goudy old style", 15, "bold"), fg="black").place(x=20, y=170)
                    elif (option == 3):
                        if(class_roman_to_numerical[sel_classS.get()]== 11 or class_roman_to_numerical[sel_classS.get()]== 12):
                            section_label = Label(add_marks_top,text="Stream", font=("Goudy old style", 15, "bold"), fg="black").place(x=20,y=80)
                        elif(class_roman_to_numerical[sel_classS.get()]!= 11 or class_roman_to_numerical[sel_classS.get()]!= 12):
                            section_label = Label(add_marks_top, text="Section", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=80)
                        entermarks_lbl = Label(add_marks_top,text="Enter Final Marks", font=("Goudy old style", 15, "bold"), fg="black").place(x=20, y=170)

            def update_marks(option):
                def update(opt,marks):
                    if (opt == 1):
                        if (class_roman_to_numerical[sel_classS.get()] == 11 or class_roman_to_numerical[
                            sel_classS.get()] == 12):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE SENIOR set BENGALI_UNIT = :benu WHERE USER_ROLL = :roll",
                                          {'benu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE SENIOR set ENGLISH_UNIT = :engu WHERE USER_ROLL = :roll",
                                          {'engu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE SENIOR set HISTORY_UNIT = :hisu WHERE USER_ROLL = :roll",
                                          {'hisu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Philosophy"):
                                c.execute("UPDATE SENIOR set PHILOSOPHY_UNIT = :phiu WHERE USER_ROLL = :roll",
                                          {'phiu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE SENIOR set GEOGRAPHY_UNIT = :geou WHERE USER_ROLL = :roll",
                                          {'geou': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Education"):
                                c.execute("UPDATE SENIOR set EDUCATION_UNIT = :eduu WHERE USER_ROLL = :roll",
                                          {'eduu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Political Science"):
                                c.execute("UPDATE SENIOR set POLITICAL_UNIT = :polu WHERE USER_ROLL = :roll",
                                          {'polu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Business Studies"):
                                c.execute("UPDATE SENIOR set BUSINESS_UNIT = :busu WHERE USER_ROLL = :roll",
                                          {'busu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Economics"):
                                c.execute("UPDATE SENIOR set ECONOMICS_UNIT = :ecou WHERE USER_ROLL = :roll",
                                          {'ecou': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Accountancy"):
                                c.execute("UPDATE SENIOR set ACCOUNT_UNIT = :accu WHERE USER_ROLL = :roll",
                                          {'accu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Law and Audit"):
                                c.execute("UPDATE SENIOR set LAW_UNIT = :lawu WHERE USER_ROLL = :roll",
                                          {'lawu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Application"):
                                c.execute("UPDATE SENIOR set COMA_UNIT = :comau WHERE USER_ROLL = :roll",
                                          {'comau': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physics"):
                                c.execute("UPDATE SENIOR set PHYSICS_UNIT = :physu WHERE USER_ROLL = :roll",
                                          {'physu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Chemistry"):
                                c.execute("UPDATE SENIOR set CHEMISTRY_UNIT = :chemu WHERE USER_ROLL = :roll",
                                          {'chemu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE SENIOR set MATH_UNIT = :mathu WHERE USER_ROLL = :roll",
                                          {'mathu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Biology"):
                                c.execute("UPDATE SENIOR set BIOLOGY_UNIT = :biou WHERE USER_ROLL = :roll",
                                          {'biou': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Science"):
                                c.execute("UPDATE SENIOR set COMS_UNIT = :comsu WHERE USER_ROLL = :roll",
                                          {'comsu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                        elif (class_roman_to_numerical[sel_classS.get()] >= 5 and class_roman_to_numerical[sel_classS.get()] <= 10):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE MIDDLE set BENGALI_UNIT = :benu WHERE USER_ROLL = :roll",
                                          {'benu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE MIDDLE set ENGLISH_UNIT = :engu WHERE USER_ROLL = :roll",
                                          {'engu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE MIDDLE set MATH_UNIT = :mathu WHERE USER_ROLL = :roll",
                                          {'mathu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE MIDDLE set HISTORY_UNIT = :hisu WHERE USER_ROLL = :roll",
                                          {'hisu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE MIDDLE set GEOGRAPHY_UNIT = :geou WHERE USER_ROLL = :roll",
                                          {'geou': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physical Science"):
                                c.execute("UPDATE MIDDLE set PHYS_UNIT = :phyu WHERE USER_ROLL = :roll",
                                          {'phyu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Life Science"):
                                c.execute("UPDATE MIDDLE set LIFE_UNIT = :lifu WHERE USER_ROLL = :roll",
                                          {'lifu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                        elif (class_roman_to_numerical[sel_classS.get()] < 5):
                            if(str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE JUNIOR set BENGALI_UNIT = :benu WHERE USER_ROLL = :roll",
                                    {'benu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif(str(sel_subD.get()) == "English"):
                                c.execute("UPDATE JUNIOR set ENGLISH_UNIT = :engu WHERE USER_ROLL = :roll",
                                          {'engu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif(str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE JUNIOR set MATH_UNIT = :mathu WHERE USER_ROLL = :roll",
                                          {'mathu': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif(str(sel_subD.get()) == "GK"):
                                c.execute("UPDATE JUNIOR set GK_UNIT = :gku WHERE USER_ROLL = :roll",
                                          {'gku': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()

                    elif (opt == 2):
                        if (class_roman_to_numerical[sel_classS.get()] == 11 or class_roman_to_numerical[sel_classS.get()] == 12):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE SENIOR set BENGALI_HALF = :benh WHERE USER_ROLL = :roll",
                                          {'benh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE SENIOR set ENGLISH_HALF = :engh WHERE USER_ROLL = :roll",
                                          {'engh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE SENIOR set HISTORY_HALF = :hish WHERE USER_ROLL = :roll",
                                          {'hish': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Philosophy"):
                                c.execute("UPDATE SENIOR set PHILOSOPHY_HALF = :phih WHERE USER_ROLL = :roll",
                                          {'phih': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE SENIOR set GEOGRAPHY_HALF = :geoh WHERE USER_ROLL = :roll",
                                          {'geoh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Education"):
                                c.execute("UPDATE SENIOR set EDUCATION_HALF = :eduh WHERE USER_ROLL = :roll",
                                          {'eduh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Political Science"):
                                c.execute("UPDATE SENIOR set POLITICAL_HALF = :polh WHERE USER_ROLL = :roll",
                                          {'polh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Business Studies"):
                                c.execute("UPDATE SENIOR set BUSINESS_HALF = :bush WHERE USER_ROLL = :roll",
                                          {'bush': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Economics"):
                                c.execute("UPDATE SENIOR set ECONOMICS_HALF = :ecoh WHERE USER_ROLL = :roll",
                                          {'ecoh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Accountancy"):
                                c.execute("UPDATE SENIOR set ACCOUNT_HALF = :acch WHERE USER_ROLL = :roll",
                                          {'acch': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Law and Audit"):
                                c.execute("UPDATE SENIOR set LAW_HALF = :lawh WHERE USER_ROLL = :roll",
                                          {'lawh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Application"):
                                c.execute("UPDATE SENIOR set COMA_HALF = :comah WHERE USER_ROLL = :roll",
                                          {'comah': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physics"):
                                c.execute("UPDATE SENIOR set PHYSICS_HALF = :physh WHERE USER_ROLL = :roll",
                                          {'physh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Chemistry"):
                                c.execute("UPDATE SENIOR set CHEMISTRY_HALF = :chemh WHERE USER_ROLL = :roll",
                                          {'chemh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE SENIOR set MATH_HALF = :mathh WHERE USER_ROLL = :roll",
                                          {'mathh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Biology"):

                                c.execute("UPDATE SENIOR set BIOLOGY_HALF = :bioh WHERE USER_ROLL = :roll",
                                          {'bioh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Science"):
                                c.execute("UPDATE SENIOR set COMS_HALF = :comsh WHERE USER_ROLL = :roll",
                                          {'comsh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                        elif (class_roman_to_numerical[sel_classS.get()] >= 5 and class_roman_to_numerical[sel_classS.get()] <= 10):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE MIDDLE set BENGALI_HALF = :benh WHERE USER_ROLL = :roll",
                                          {'benh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE MIDDLE set ENGLISH_HALF = :engh WHERE USER_ROLL = :roll",
                                          {'engh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE MIDDLE set MATH_HALF = :mathh WHERE USER_ROLL = :roll",
                                          {'mathh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE MIDDLE set HISTORY_HALF = :hish WHERE USER_ROLL = :roll",
                                          {'hish': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE MIDDLE set GEOGRAPHY_HALF = :geoh WHERE USER_ROLL = :roll",
                                          {'geoh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physical Science"):
                                c.execute("UPDATE MIDDLE set PHYS_HALF = :phyh WHERE USER_ROLL = :roll",
                                          {'phyh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Life Science"):
                                c.execute("UPDATE MIDDLE set LIFE_HALF = :lifh WHERE USER_ROLL = :roll",
                                          {'lifh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                        elif(class_roman_to_numerical[sel_classS.get()] < 5):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE JUNIOR set BENGALI_HALF = :benh WHERE USER_ROLL = :roll",
                                        {'benh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE JUNIOR set ENGLISH_HALF = :engh WHERE USER_ROLL = :roll", {'engh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE JUNIOR set MATH_HALF = :mathh WHERE USER_ROLL = :roll", {'mathh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "GK"):
                                c.execute("UPDATE JUNIOR set GK_HALF = :gkh WHERE USER_ROLL = :roll", {'gkh': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()

                    elif (opt == 3):
                        if (class_roman_to_numerical[sel_classS.get()] == 11 or class_roman_to_numerical[sel_classS.get()] == 12):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE SENIOR set BENGALI_FINAL = :benf WHERE USER_ROLL = :roll",
                                          {'benf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE SENIOR set ENGLISH_FINAL = :engf WHERE USER_ROLL = :roll",
                                          {'engf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE SENIOR set HISTORY_FINAL = :hisf WHERE USER_ROLL = :roll",
                                          {'hisf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Philosophy"):
                                c.execute("UPDATE SENIOR set PHILOSOPHY_FINAL = :phif WHERE USER_ROLL = :roll",
                                          {'phif': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE SENIOR set GEOGRAPHY_FINAL = :geof WHERE USER_ROLL = :roll",
                                          {'geof': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Education"):
                                c.execute("UPDATE SENIOR set EDUCATION_FINAL = :eduf WHERE USER_ROLL = :roll",
                                          {'eduf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Political Science"):
                                c.execute("UPDATE SENIOR set POLITICAL_FINAL = :polf WHERE USER_ROLL = :roll",
                                          {'polf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Business Studies"):
                                c.execute("UPDATE SENIOR set BUSINESS_FINAL = :busf WHERE USER_ROLL = :roll",
                                          {'busf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Economics"):
                                c.execute("UPDATE SENIOR set ECONOMICS_FINAL = :ecof WHERE USER_ROLL = :roll",
                                          {'ecof': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Accountancy"):
                                c.execute("UPDATE SENIOR set ACCOUNT_FINAL = :accf WHERE USER_ROLL = :roll",
                                          {'accf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Law and Audit"):
                                c.execute("UPDATE SENIOR set LAW_FINAL = :lawf WHERE USER_ROLL = :roll",
                                          {'lawf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Application"):
                                c.execute("UPDATE SENIOR set COMA_FINAL = :comaf WHERE USER_ROLL = :roll",
                                          {'comaf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physics"):
                                c.execute("UPDATE SENIOR set PHYSICS_FINAL = :physf WHERE USER_ROLL = :roll",
                                          {'physf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Chemistry"):
                                c.execute("UPDATE SENIOR set CHEMISTRY_FINAL = :chemf WHERE USER_ROLL = :roll",
                                          {'chemf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE SENIOR set MATH_FINAL = :mathf WHERE USER_ROLL = :roll",
                                          {'mathf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Biology"):
                                c.execute("UPDATE SENIOR set BIOLOGY_FINAL = :biof WHERE USER_ROLL = :roll",
                                          {'biof': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Computer Science"):
                                c.execute("UPDATE SENIOR set COMS_FINAL = :comsf WHERE USER_ROLL = :roll",
                                          {'comsf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                        elif (class_roman_to_numerical[sel_classS.get()] >= 5 and class_roman_to_numerical[sel_classS.get()] <= 10):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE MIDDLE set BENGALI_FINAL = :benf WHERE USER_ROLL = :roll",
                                          {'benf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE MIDDLE set ENGLISH_FINAL = :engf WHERE USER_ROLL = :roll",
                                          {'engf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE MIDDLE set MATH_FINAL = :mathf WHERE USER_ROLL = :roll",
                                          {'mathf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "History"):
                                c.execute("UPDATE MIDDLE set HISTORY_FINAL = :hisf WHERE USER_ROLL = :roll",
                                          {'hisf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Geography"):
                                c.execute("UPDATE MIDDLE set GEOGRAPHY_FINAL = :geof WHERE USER_ROLL = :roll",
                                          {'geof': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Physical Science"):
                                c.execute("UPDATE MIDDLE set PHYS_FINAL = :phyf WHERE USER_ROLL = :roll",
                                          {'phyf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Life Science"):
                                c.execute("UPDATE MIDDLE set LIFE_FINAL = :liff WHERE USER_ROLL = :roll",
                                          {'liff': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                        elif (class_roman_to_numerical[sel_classS.get()] < 5):
                            if (str(sel_subD.get()) == "Bengali"):
                                c.execute("UPDATE JUNIOR set BENGALI_FINAL = :benf WHERE USER_ROLL = :roll",{'benf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "English"):
                                c.execute("UPDATE JUNIOR set ENGLISH_FINAL = :engf WHERE USER_ROLL = :roll", {'engf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "Mathematics"):
                                c.execute("UPDATE JUNIOR set MATH_FINAL = :mathf WHERE USER_ROLL = :roll", {'mathf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()
                            elif (str(sel_subD.get()) == "GK"):
                                c.execute("UPDATE JUNIOR set GK_FINAL = :gkf WHERE USER_ROLL = :roll", {'gkf': int(marks), 'roll': int(user_sel[0])})
                                conn.commit()

                    update_marks_top.destroy()

                sel_row = marksentry_tree.selection()
                if (len(sel_row) > 1):
                    tmg.showwarning("Error", "Please select One Student !", parent=Frame_right)
                elif (len(sel_row) == 0):
                    tmg.showwarning("Error", "Please select One Student to update marks !", parent=Frame_right)
                else:
                    user_sel = marksentry_tree.item(sel_row, 'values')
                    update_marks_top = Toplevel(Frame_right)
                    update_marks_top.title("Update Marks")
                    update_marks_top.geometry("550x290+0+0")
                    update_marks_top.resizable(False, False)
                    TOP_BG = Label(update_marks_top, image=bgtop3)
                    TOP_BG.place(x=0, y=0, relwidth=1, relheight=1)

                    marks = str(0)
                    marksS = StringVar()
                    marksS.set(marks)
                    name_lbl = Label(update_marks_top, text="Name", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=20)
                    nameE_lbl = Label(update_marks_top, text=str(user_sel[1]), font=("Goudy old style", 15, "bold"),fg="black").place(x=250, y=20)
                    class_lbl = Label(update_marks_top, text="Class", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=50)
                    classE_lbl = Label(update_marks_top, text=str(class_roman_to_numerical[sel_classS.get()]),font=("Goudy old style", 15, "bold"), fg="black").place(x=250, y=50)
                    secE_lbl = Label(update_marks_top, text=str(sel_secD.get()), font=("Goudy old style", 15, "bold"),fg="black").place(x=250, y=80)
                    roll_label = Label(update_marks_top, text="Roll No", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=110)
                    rollE_lbl = Label(update_marks_top, text=str(user_sel[0]), font=("Goudy old style", 15, "bold"),fg="black").place(x=250, y=110)
                    subject_lbl = Label(update_marks_top, text="Subject", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=140)
                    subjectE_lbl = Label(update_marks_top, text=str(sel_subD.get()), font=("Goudy old style", 15, "bold"),fg="black").place(x=250, y=140)
                    entermarksE = Entry(update_marks_top, textvariable=marksS, font=("times new roman", 15),bg="light grey")
                    entermarksE.place(x=250, y=170, width=100, height=30)
                    update_button = Button(update_marks_top, command=lambda: update(option, str(marksS.get())), text="Update",fg="black", bg="sky blue",font=("times new roman", 15))
                    update_button.place(x=80, y=220, height=30, width=80)
                    cancel_button = Button(update_marks_top, command=update_marks_top.destroy, text="Cancel", fg="black",bg="sky blue", font=("times new roman", 15))
                    cancel_button.place(x=250, y=220, height=30, width=80)
                    if (option == 1):
                        if (class_roman_to_numerical[sel_classS.get()] == 11 or class_roman_to_numerical[sel_classS.get()] == 12):
                            section_label = Label(update_marks_top, text="Stream", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=80)
                        elif (class_roman_to_numerical[sel_classS.get()] != 11 or class_roman_to_numerical[sel_classS.get()] != 12):
                            section_label = Label(update_marks_top, text="Section", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=80)
                        entermarks_lbl = Label(update_marks_top, text="Enter Unit Marks",font=("Goudy old style", 15, "bold"), fg="black").place(x=20, y=170)
                    elif (option == 2):
                        if (class_roman_to_numerical[sel_classS.get()] == 11 or class_roman_to_numerical[sel_classS.get()] == 12):
                            section_label = Label(update_marks_top, text="Stream", font=("Goudy old style", 15, "bold"),
                                            fg="black").place(x=20, y=80)
                        elif (class_roman_to_numerical[sel_classS.get()] != 11 or class_roman_to_numerical[
                            sel_classS.get()] != 12):
                            section_label = Label(update_marks_top, text="Section", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=80)
                        entermarks_lbl = Label(update_marks_top, text="Enter Half Yearly Marks",font=("Goudy old style", 15, "bold"), fg="black").place(x=20, y=170)
                    elif (option == 3):
                        if (class_roman_to_numerical[sel_classS.get()] == 11 or class_roman_to_numerical[sel_classS.get()] == 12):
                            section_label = Label(update_marks_top, text="Stream", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=80)
                        elif (class_roman_to_numerical[sel_classS.get()] != 11 or class_roman_to_numerical[sel_classS.get()] != 12):
                            section_label = Label(update_marks_top, text="Section", font=("Goudy old style", 15, "bold"),fg="black").place(x=20, y=80)
                        entermarks_lbl = Label(update_marks_top, text="Enter Final Marks",font=("Goudy old style", 15, "bold"), fg="black").place(x=20, y=170)

            class_roman_to_numerical = {"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,"IX":9,"X":10,"XI":11,"XII":12}
            if(sel_classD.get() == "" or sel_secD.get()=="" or sel_subD.get()==""):
                tmg.showwarning("Error", "All fields are required !", parent=Frame_right)
            else:
                FR_BG.configure(image=bg9)
                global check
                check = str(class_roman_to_numerical[sel_classS.get()])

                showing_tree_lbl.configure(text="Showing Data of "+ str(sel_classD.get()) + " ➖ " + str(sel_secD.get()) + "➖ " + str(sel_subD.get()))
                showing_tree_lbl.place(x=20, y=140)
                marksentry_tree = ttk.Treeview(Frame_right,height=15)
                marksentry_tree.pack()
                marksentry_tree_yscroll= ttk.Scrollbar(Frame_right,orient="vertical", command=marksentry_tree.yview)
                marksentry_tree_yscroll.place(x=450,y=200,height=320)
                marksentry_tree.config(yscrollcommand=marksentry_tree_yscroll.set)
                marksentry_tree.pack()
                marksentry_tree['columns'] = ("Roll No.", "Name")
                marksentry_tree['show'] = 'headings'
                marksentry_tree.column("#0", anchor=W, width=0, stretch=NO)
                marksentry_tree.column("Roll No.", anchor=W, width=100)
                marksentry_tree.column("Name", anchor=W, width=320)
                marksentry_tree.heading("#0", text="#", anchor=W)
                marksentry_tree.heading("Roll No.", text="Roll No.", anchor=W)
                marksentry_tree.heading("Name", text="Name", anchor=W)
                if (int(check) < 5):
                    c.execute("SELECT JT FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                    d = c.fetchall()
                    if (d[0][0] == 1):
                        c.execute("SELECT * FROM JUNIOR")
                        data = c.fetchall()
                        global count
                        count = 0
                        roll = []
                        for record in data:
                            if(record[1]==class_roman_to_numerical[sel_classS.get()] and record[2]==sel_sectionS.get()):
                                marksentry_tree.insert(parent='', index='end', iid=count, text=(count + 1),
                                                   values=(record[3], record[0]))
                                count += 1
                                roll.append(record[3])

                elif ((int(check) >= 5) and (int(check) <= 10)):
                    c.execute("SELECT MT FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                    d = c.fetchall()
                    if(d[0][0] == 1):
                        c.execute("SELECT * FROM MIDDLE")
                        data = c.fetchall()
                        count = 0
                        roll = []
                        for record in data:
                            if(record[1]==class_roman_to_numerical[sel_classS.get()] and record[2]==sel_sectionS.get()):
                                marksentry_tree.insert(parent='', index='end', iid=count, text=(count + 1),
                                       values=(record[3], record[0]))
                                count += 1
                                roll.append(record[3])
                else:
                    c.execute("SELECT ST FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                    d = c.fetchall()
                    if(d[0][0] == 1):
                        c.execute("SELECT * FROM SENIOR")
                        data = c.fetchall()
                        count = 0
                        roll = []
                        optional_subject_dict= {"Arts":["Education","Political Science"],"Commerce":["Law and Audit", "Computer Application"],"Science":["Biology", "Computer Science"]}
                        for record in data:
                            keylist_opt_sub = optional_subject_dict[str(sel_sectionS.get())]
                            if(str(sel_subjectS.get()) in keylist_opt_sub):
                                check_opt=str(sel_subjectS.get())
                                if (record[1] == class_roman_to_numerical[sel_classS.get()] and record[2] == sel_sectionS.get() and record[10]==check_opt):
                                    marksentry_tree.insert(parent='', index='end', iid=count, text=(count + 1),values=(record[3], record[0]))
                                    count += 1
                                    roll.append(record[3])
                            elif(record[1]==class_roman_to_numerical[sel_classS.get()] and record[2]==sel_sectionS.get()):
                                marksentry_tree.insert(parent='', index='end', iid=count, text=(count + 1),values=(record[3], record[0]))
                                count += 1
                                roll.append(record[3])
                marksentry_tree.pack()
                marksentry_tree.place(x=20,y=200)

                add_lbl.configure(text="ADD MARKS")
                add_lbl.place(x=630,y=170)
                add_utmarks_button.configure(command=lambda: add_marks(1))
                add_hmarks_button.configure(command=lambda: add_marks(2))
                add_fmarks_button.configure(command=lambda: add_marks(3))
                add_utmarks_button.place(x=600, y=210, height=35, width=200)
                add_hmarks_button.place(x=600, y=260, height=35, width=200)
                add_fmarks_button.place(x=600, y=310, height=35, width=200)

                update_lbl.configure(text="UPDATE MARKS")
                update_lbl.place(x=620,y=380)
                update_utmarks_button.configure(command = lambda: update_marks(1))
                update_hmarks_button.configure(command=lambda: update_marks(2))
                update_fmarks_button.configure(command=lambda: update_marks(3))
                update_utmarks_button.place(x=600, y=420, height=35, width=200)
                update_hmarks_button.place(x=600, y=470, height=35, width=200)
                update_fmarks_button.place(x=600, y=520, height=35, width=200)

        global Frame_right
        Frame_right.destroy()
        Frame_right = Frame(root)
        Frame_right.place(x=350, y=60, height=600, width=900)
        FR_BG = Label(Frame_right, image=bg8)
        FR_BG.place(x=0, y=0, relwidth=1, relheight=1)
        sel_classS =StringVar()
        sel_sectionS = StringVar()
        sel_subjectS= StringVar()
        selected_lbl = Label(Frame_right, text="Selected Class None ➖ Section None ➖ Subject None",font=("Goudy old style", 20, "bold"), fg="black")
        selected_lbl.place(x=20, y=20)
        r_class= ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"]
        class_lbl = Label(Frame_right, text="Class", font=("Goudy old style", 20, "bold"), fg="black").place(x=20, y=65)
        sel_classD=ttk.Combobox(Frame_right, textvariable=sel_classS,font=(20),value=r_class, state="readonly")
        sel_classD.place(x=100, y=65, width=100, height=35)
        sel_classD.bind("<<ComboboxSelected>>",comboclick1)
        section_label= Label(Frame_right, text="Section", font=("Goudy old style", 20, "bold"), fg="black")
        section_label.place(x=230, y=65)
        sel_secD = ttk.Combobox(Frame_right, textvariable=sel_sectionS, font=(25),state="readonly")
        sel_secD.place(x=330, y=65, width=100, height=35)
        sel_secD.bind("<<ComboboxSelected>>", comboclick2)
        sub_lbl= Label(Frame_right, text="Subject", font=("Goudy old style", 20, "bold"), fg="black")
        sub_lbl.place(x=450, y=65, width=100, height=35)
        sel_subD= ttk.Combobox(Frame_right, textvariable=sel_subjectS, font=(25),state="readonly")
        sel_subD.place(x=550, y=65, width=200, height=35)
        sel_subD.bind("<<ComboboxSelected>>", comboclick3)
        showing_tree_lbl = Label(Frame_right, font=("Goudy old style", 15, "bold"), fg="black")
        go_bt= Button(Frame_right,command=go ,text="GO➡", fg="black",bg="sky blue", font=("times new roman", 15))
        go_bt.place(x=780, y=65, height=35, width=100)
        add_lbl= Label(Frame_right, font=("Goudy old style", 15, "bold"), fg="black")
        add_utmarks_button = Button(Frame_right, text="Unit Test",fg="white", bg="#d77337", font=("times new roman", 15))
        add_hmarks_button = Button(Frame_right,  text="Half Yearly", fg="white", bg="#d77337",font=("times new roman", 15))
        add_fmarks_button = Button(Frame_right,  text="Final", fg="white", bg="#d77337",font=("times new roman", 15))
        update_lbl= Label(Frame_right, font=("Goudy old style", 15, "bold"), fg="black")
        update_utmarks_button = Button(Frame_right, text="Unit Test", fg="white", bg="#d77337",font=("times new roman", 15))
        update_hmarks_button = Button(Frame_right,  text="Half Yearly", fg="white", bg="#d77337",font=("times new roman", 15))
        update_fmarks_button = Button(Frame_right,  text="Final", fg="white", bg="#d77337",font=("times new roman", 15))

    def result():
        def result_class(class_no,class_roman):

            def show_table():
                def show_result():
                    sel_row = class_view_tree.selection()
                    if (len(sel_row) > 1):
                        tmg.showwarning("Error", "Please select One Student !", parent=Frame_right)
                    elif (len(sel_row) == 0):
                        tmg.showwarning("Error", "Please select One Student !",parent=Frame_right)
                    else:
                        user_sel = class_view_tree.item(sel_row, 'values')
                        show_top = Toplevel(Frame_right)
                        show_top.title("Show Marks")
                        show_top.geometry("600x400+0+0")
                        show_top.resizable(False, False)
                        TOP_BG = Label(show_top, image=bgtop4)
                        TOP_BG.place(x=0, y=0, relwidth=1, relheight=1)
                        name_lbl = Label(show_top, text="Name", font=("Goudy old style", 15, "bold"),fg="black").place(x=50, y=20)
                        studentname_lbl = Label(show_top, text=str(user_sel[1]),font=("Goudy old style", 15, "bold"), fg="black").place(x=150, y=20)
                        class_lbl = Label(show_top, text="Class", font=("Goudy old style", 15, "bold"),fg="black").place(x=50, y=60)
                        class_r_lbl = Label(show_top, text=str(class_roman),font=("Goudy old style", 15, "bold"), fg="black").place(x=150, y=60)
                        roll_label = Label(show_top, text="Roll No.", font=("Goudy old style", 15, "bold"),fg="black").place(x=50, y=100)
                        roll_r_lbl = Label(show_top, text=str(user_sel[0]), font=("Goudy old style", 15, "bold"),fg="black").place(x=150, y=100)

                        cancel_button= Button(show_top, command=show_top.destroy, text="Cancel", fg="black", bg="sky blue", font=("times new roman", 15))
                        cancel_button.place(x=260, y=350, height=30, width=80)

                        result_tree = ttk.Treeview(show_top, height=8)
                        result_tree.pack()
                        result_tree.pack()
                        result_tree['columns'] = ("Subject", "Unit Test","Half Yearly Test","Final Test")
                        result_tree['show'] = 'headings'
                        result_tree.column("#0", anchor=W, width=0, stretch=NO)
                        result_tree.column("Subject", anchor=W, width=200)
                        result_tree.column("Unit Test", anchor=W, width=100)
                        result_tree.column("Half Yearly Test", anchor=W, width=100)
                        result_tree.column("Final Test", anchor=W, width=100)
                        result_tree.heading("#0", text="#", anchor=W)
                        result_tree.heading("Subject", text="Subject", anchor=W)
                        result_tree.heading("Unit Test", text="Unit Test", anchor=W)
                        result_tree.heading("Half Yearly Test", text="Half Yearly Test", anchor=W)
                        result_tree.heading("Final Test", text="Final Test", anchor=W)
                        if(class_no>10):
                            if(section_selS.get()=="Arts"):
                                index = roll.index(int(user_sel[0]))
                                values = ["Bengali", "English", "History", "Philosophy", "Geography"]
                                record = [[values[0], data[index][11], data[index][12], data[index][13]],
                                          [values[1], data[index][14], data[index][15], data[index][16]],
                                          [values[2], data[index][17], data[index][18], data[index][19]],
                                          [values[3], data[index][20], data[index][21], data[index][22]],
                                          [values[4], data[index][23], data[index][24], data[index][25]]]
                                if(str(data[index][10]) == "Education"):
                                    values.append("Education")
                                    record.append([values[5], data[index][26], data[index][27], data[index][28]])
                                elif(str(data[index][10]) == "Political Science"):
                                    values.append("Political Science")
                                    record.append([values[5],data[index][29],data[index][30],data[index][31]])
                                count = 0
                                for record in record:
                                    result_tree.insert(parent='', index='end', iid=count, text=(count + 1),values=(record[0], record[1],record[2],record[3]))
                                    count += 1
                                result_tree.pack()
                                result_tree.place(x=50, y=150)
                            elif (section_selS.get() == "Commerce"):
                                index = roll.index(int(user_sel[0]))
                                values = ["Bengali", "English", "Business Studies","Economics", "Accountancy"]
                                record = [[values[0], data[index][11], data[index][12], data[index][13]],
                                          [values[1], data[index][14], data[index][15], data[index][16]],
                                          [values[2], data[index][32], data[index][33], data[index][34]],
                                          [values[3], data[index][35], data[index][36], data[index][37]],
                                          [values[4], data[index][38], data[index][39], data[index][40]]]
                                if (str(data[index][10])== "Law and Audit"):
                                    values.append("Law and Audit")
                                    record.append([values[5], data[index][41], data[index][42], data[index][43]])
                                elif (str(data[index][10])=="Computer Application"):
                                    values.append("Computer Application")
                                    record.append([values[5], data[index][44], data[index][45], data[index][46]])
                                count = 0
                                for record in record:
                                    result_tree.insert(parent='', index='end', iid=count, text=(count + 1),values=(record[0], record[1], record[2], record[3]))
                                    count += 1
                                result_tree.pack()
                                result_tree.place(x=50, y=150)
                            elif(section_selS.get() == "Science"):
                                index = roll.index(int(user_sel[0]))
                                values = ["Bengali", "English","Physics", "Chemistry", "Mathematics"]
                                record = [[values[0], data[index][11], data[index][12], data[index][13]],
                                          [values[1], data[index][14], data[index][15], data[index][16]],
                                          [values[2], data[index][47], data[index][48], data[index][49]],
                                          [values[3], data[index][50], data[index][51], data[index][52]],
                                          [values[4], data[index][53], data[index][54], data[index][55]]]
                                if (str(data[index][10]) == "Biology"):
                                    values.append("Biology")
                                    record.append([values[5], data[index][56], data[index][57], data[index][58]])
                                elif (str(data[index][10])=="Computer Science" ):
                                    values.append("Computer Science")
                                    record.append([values[5], data[index][59], data[index][60], data[index][61]])
                                count = 0
                                for record in record:
                                    result_tree.insert(parent='', index='end', iid=count, text=(count + 1),values=(record[0], record[1], record[2], record[3]))
                                    count += 1
                                result_tree.pack()
                                result_tree.place(x=50, y=150)
                        elif(class_no<=10 and class_no>4):
                            index = roll.index(int(user_sel[0]))
                            values = ["Bengali", "English","Mathematics","History", "Geography", "Physical Science", "Life Science"]
                            record = [[values[0], data[index][10], data[index][11], data[index][12]],
                                      [values[1], data[index][13], data[index][14], data[index][15]],
                                      [values[2], data[index][16], data[index][17], data[index][18]],
                                      [values[3], data[index][19], data[index][20], data[index][21]],
                                      [values[4], data[index][22], data[index][23], data[index][24]],
                                      [values[5], data[index][25], data[index][26], data[index][27]],
                                      [values[5], data[index][28], data[index][29], data[index][30]]]
                            count = 0
                            for record in record:
                                result_tree.insert(parent='', index='end', iid=count, text=(count + 1),
                                                   values=(record[0], record[1], record[2], record[3]))
                                count += 1
                            result_tree.pack()
                            result_tree.place(x=50, y=150)
                        else:
                            index = roll.index(int(user_sel[0]))
                            values = ["Bengali", "English", "Mathematics", "GK"]
                            record = [[values[0], data[index][10], data[index][11], data[index][12]], [values[1], data[index][13], data[index][14], data[index][15]], [values[2], data[index][16], data[index][17], data[index][18]],
                                      [values[3], data[index][19], data[index][20], data[index][21]]]

                            count = 0
                            for record in record:
                                result_tree.insert(parent='', index='end', iid=count, text=(count + 1),
                                                   values=(record[0], record[1],record[2],record[3]))
                                count += 1
                            result_tree.pack()
                            result_tree.place(x=50, y=150)

                show_button = Button(Frame_right, command=show_result, text="Show Marks", fg="white", bg="#d77337",font=("times new roman", 15))
                show_button.place(x=600, y=300, height=35, width=200)
                class_view_tree = ttk.Treeview(Frame_right, height=15)
                class_view_tree.pack()
                class_view_tree_yscroll = ttk.Scrollbar(Frame_right, orient="vertical", command=class_view_tree.yview)
                class_view_tree_yscroll.place(x=480, y=150, height=320)
                class_view_tree.config(yscrollcommand=class_view_tree_yscroll.set)
                class_view_tree.pack()
                class_view_tree['columns'] = ("Roll No.", "Name")
                class_view_tree['show'] = 'headings'
                class_view_tree.column("#0", anchor=W, width=0, stretch=NO)
                class_view_tree.column("Roll No.", anchor=W, width=100)
                class_view_tree.column("Name", anchor=W, width=320)
                class_view_tree.heading("#0", text="#", anchor=W)
                class_view_tree.heading("Roll No.", text="Roll No.", anchor=W)
                class_view_tree.heading("Name", text="Name", anchor=W)
                if (int(class_no) < 5):
                    c.execute("SELECT JT FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                    d = c.fetchall()
                    if (d[0][0] == 1):
                        c.execute("SELECT * FROM JUNIOR")
                        data = c.fetchall()
                        global count
                        count = 0
                        roll = []
                        for record in data:
                            roll.append(record[3])
                            if(record[1] == class_no  and record[2] == str(section_selS.get())):
                                class_view_tree.insert(parent='', index='end', iid=count, text=(count + 1),
                                                   values=(record[3], record[0]))
                                count += 1
                            showing_tree_lbl.configure(text="Showing Data of " + str(count) + " Students of Class " + str(
                                    class_roman) + " ➖ " + str(section_selS.get()))
                            showing_tree_lbl.place(x=50, y=120)
                    else:
                        showing_tree_lbl.configure(text="Showing Data of " + str(0) + " Students of " + str(
                            class_roman) + " ➖ " + str(section_selS.get()))
                        showing_tree_lbl.place(x=50, y=120)

                elif ((int(class_no) >= 5) and (int(class_no) <= 10)):
                    c.execute("SELECT MT FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                    d = c.fetchall()
                    if(d[0][0] == 1):
                        c.execute("SELECT * FROM MIDDLE")
                        data = c.fetchall()
                        count = 0
                        roll = []
                        for record in data:
                            roll.append(record[3])
                            if(record[1] == class_no and record[2] == str(section_selS.get())):
                                class_view_tree.insert(parent='', index='end', iid=count, text=(count + 1),
                                       values=(record[3], record[0]))
                                count += 1
                            showing_tree_lbl.configure(text="Showing Data of " + str(count) + " Students of " + str(
                                class_roman) + " ➖ " + str(section_selS.get()))
                            showing_tree_lbl.place(x=20, y=120)
                    else:
                        showing_tree_lbl.configure(text="Showing Data of " + str(0) + " Students of " + str(
                            class_roman) + " ➖ " + str(section_selS.get()))
                        showing_tree_lbl.place(x=50, y=120)
                else:
                    c.execute("SELECT ST FROM USER WHERE USER_ID = :name", {'name': user_data[0]})
                    d = c.fetchall()
                    if(d[0][0] == 1):
                        c.execute("SELECT * FROM SENIOR")
                        data = c.fetchall()
                        count = 0
                        roll = []
                        for record in data:
                            roll.append(record[3])
                            if(record[1] == class_no and record[2] == str(section_selS.get())):
                                class_view_tree.insert(parent='', index='end', iid=count, text=(count + 1),
                                       values=(record[3], record[0]))
                                count += 1
                            showing_tree_lbl.configure(text="Showing Data of " + str(count) + " Students of " + str(
                                class_roman) + " ➖ " + str(section_selS.get()))
                            showing_tree_lbl.place(x=50, y=120)
                    else:
                        showing_tree_lbl.configure(text="Showing Data of " + str(0) + " Students of " + str(
                            class_roman) + " ➖ " + str(section_selS.get()))
                        showing_tree_lbl.place(x=50, y=120)
                class_view_tree.pack()
                class_view_tree.place(x=50, y=150)

            global Frame_right
            Frame_right.destroy()
            Frame_right = Frame(root)
            Frame_right.place(x=350, y=60, height=600, width=900)
            FR_BG = Label(Frame_right, image=bg10)
            FR_BG.place(x=0, y=0, relwidth=1, relheight=1)
            section_selS = StringVar()
            class_lbl = Label(Frame_right, font=("Goudy old style", 15, "bold"), fg="black")
            section_label = Label(Frame_right, font=("Goudy old style", 15, "bold"), fg="black")
            select_secD = ttk.Combobox(Frame_right, textvariable=section_selS, font=(15), state="readonly")
            showing_tree_lbl = Label(Frame_right, font=("Goudy old style", 15, "bold"), fg="black")
            if (class_no <= 10):
                class_lbl.configure(text=("Class "+str(class_roman)))
                class_lbl.place(x=200, y=30)
                section_label.configure(text="Section")
                section_label.place(x=320, y=30)
                select_secD.configure(value=["A", "B", "C"])
                select_secD.place(x=390, y=30, width=100, height=30)
                select_secD.current(0)
                go_button = Button(Frame_right, command=show_table, text="GO➡", fg="black", bg="sky blue",font=("times new roman", 15))
                go_button.place(x=570, y=30, height=35, width=100)
            elif (class_no > 10):
                class_lbl.configure(text=("Class " + str(class_roman)))
                class_lbl.place(x=200, y=30)
                section_label.configure(text="Stream")
                section_label.place(x=300, y=30)
                select_secD.configure(value=["Arts", "Commerce", "Science"])
                select_secD.place(x=390, y=30, width=100, height=30)
                select_secD.current(0)
                go_button = Button(Frame_right, command=show_table, text="GO➡", fg="black", bg="sky blue",font=("times new roman", 15))
                go_button.place(x=570, y=30, height=35, width=100)

        global Frame_right
        Frame_right.destroy()
        Frame_right = Frame(root)
        Frame_right.place(x=350, y=60, height=600, width=900)
        FR_BG = Label(Frame_right, image=bg5)
        FR_BG.place(x=0, y=0, relwidth=1, relheight=1)
        sel_class_lbl = Label(Frame_right, text="Select Class to View Result", font=("Goudy old style", 25, "bold"), fg="black").place(x=285, y=20)
        class1_button = Button(Frame_right, command=lambda: result_class(1, "I"), text="Class I", fg="black",
                            bg="sky blue", font=("times new roman", 15))
        class1_button.place(x=180, y=100, height=40, width=100)
        class2_button = Button(Frame_right, command=lambda: result_class(2, "II"), text="Class II", fg="black",
                            bg="sky blue", font=("times new roman", 15))
        class2_button.place(x=400, y=100, height=40, width=100)
        class3_button = Button(Frame_right, command=lambda: result_class(3, "III"), text="Class III", fg="black",
                            bg="sky blue", font=("times new roman", 15))
        class3_button.place(x=620, y=100, height=40, width=100)
        class4_button = Button(Frame_right, command=lambda: result_class(4, "IV"), text="Class IV", fg="black",
                            bg="sky blue", font=("times new roman", 15))
        class4_button.place(x=180, y=210, height=40, width=100)
        class5_button = Button(Frame_right, command=lambda: result_class(5, "V"), text="Class V", fg="black",
                            bg="sky blue", font=("times new roman", 15))
        class5_button.place(x=400, y=210, height=40, width=100)
        class6_button = Button(Frame_right, command=lambda: result_class(6, "VI"), text="Class VI", fg="black",
                            bg="sky blue", font=("times new roman", 15))
        class6_button.place(x=620, y=210, height=40, width=100)
        class7_button = Button(Frame_right, command=lambda: result_class(7, "VII"), text="Class VII", fg="black",
                            bg="sky blue", font=("times new roman", 15))
        class7_button.place(x=180, y=320, height=40, width=100)
        class8_button = Button(Frame_right, command=lambda: result_class(8, "VIII"), text="Class VIII", fg="black",
                            bg="sky blue", font=("times new roman", 15))
        class8_button.place(x=400, y=320, height=40, width=100)
        class9_button = Button(Frame_right, command=lambda: result_class(9, "IX"), text="Class IX", fg="black",
                            bg="sky blue", font=("times new roman", 15))
        class9_button.place(x=620, y=320, height=40, width=100)
        class10_button = Button(Frame_right, command=lambda: result_class(10, "X"), text="Class X", fg="black",
                             bg="sky blue", font=("times new roman", 15))
        class10_button.place(x=180, y=430, height=40, width=100)
        class11_button = Button(Frame_right, command=lambda: result_class(11, "XI"), text="Class XI", fg="black",
                             bg="sky blue", font=("times new roman", 15))
        class11_button.place(x=400, y=430, height=40, width=100)
        class12_button = Button(Frame_right, command=lambda: result_class(12, "XII"), text="Class XII", fg="black",
                             bg="sky blue", font=("times new roman", 15))
        class12_button.place(x=620, y=430, height=40, width=100)

    user_info = StringVar()
    welcome_info = StringVar()
    user_info.set(user_data[1] + " , " + user_data[0])
    welcome_info.set("Welcome ! \n" + user_data[1] + " , " + user_data[0])

    global bg_image
    bg_image.configure(image=bgimagehome)
    global Frame_right
    Frame_right = Frame(root, bg="white")
    Frame_right.place(x=350, y=60, height=600, width=900)

    FR_BG = Label(Frame_right, image=bg2).place(x=0, y=0, relwidth=1, relheight=1)

    label_welcome = Label(Frame_right, textvariable=welcome_info, font=("Impact", 35, "bold"), fg="#d77337")
    label_welcome.place(x=100, y=100)

    Frame_home_left = Frame(root, bg="light grey")
    Frame_home_left.place(x=30, y=300, height=280, width=300)

    view_button = Button(Frame_home_left, command=view_portal, text="View", fg="black", bg="sky blue",
                         font=("times new roman", 15))
    data_entry_button = Button(Frame_home_left, command=data_entry, text="Data Entry", fg="black", bg="sky blue",
                               font=("times new roman", 15))
    marks_entry_button = Button(Frame_home_left, command=marks_entry, text="Marks Entry", fg="black", bg="sky blue",
                                font=("times new roman", 15))
    result_button = Button(Frame_home_left, command=result, text="Result", fg="black", bg="sky blue",
                           font=("times new roman", 15))

    view_button.place(x=35, y=35, height=30, width=230)
    data_entry_button.place(x=35, y=95, height=30, width=230)
    marks_entry_button.place(x=35, y=155, height=30, width=230)
    result_button.place(x=35, y=215, height=30, width=230)

    logout_button = Button(root, command=root.destroy, text="Logout", fg="white", bg="#d77337",
                           font=("times new roman", 15))
    logout_button.place(x=1160, y=10, height=30, width=100)

    if (user_data[1] == 'ADMIN'):
        admin_portal_button = Button(root, command=admin_portal, text="Admin Portal", fg="white", bg="#d77337",font=("times new roman", 15))
        admin_portal_button.place(x=100, y=10, height=30, width=150)

    label_user_info = Label(root, textvariable=user_info, font=("Goudy old style", 15, "bold"), fg="black", bg="white")
    label_user_info.place(x=640, y=10)

login()
root.mainloop()
conn.close()