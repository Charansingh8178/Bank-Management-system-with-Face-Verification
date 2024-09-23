import mysql.connector as sql
import tkinter as Tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image

conn = sql.connect(host='localhost', user='root', passwd='charansingh', database='bank')
c1 = conn.cursor()

if conn.is_connected():
    print("Connection is successful")
else:
    print("ERROR IN CONNECTING DATABASE")

root = Tk()
root.title("Bank Management System")
root.geometry('400x400')

img= Image.open(r'pic.jpg')

bg=ImageTk.PhotoImage(img)
background= Label(root,image=bg)
background.place(relwidth=2,relheight=2)
background.image=bg



w = Label(root, text="Welcome to\nBank Management System")
w.pack(pady=10)


def new_user_form():
    
    for widget in root.winfo_children():
        widget.destroy()
    
    Label(root, text="Enter Your Details:").pack(pady=5)

    Label(root, text="Name").pack()
    name_entry = Entry(root)
    name_entry.pack()

    Label(root, text="Contact Number").pack()
    contact_entry = Entry(root)
    contact_entry.pack()

    Label(root, text="Date of Birth (YYYY-MM-DD)").pack()
    dob_entry = Entry(root)
    dob_entry.pack()

    Label(root, text="Unique ID").pack()
    unique_id_entry = Entry(root)
    unique_id_entry.pack()

    Label(root, text="City").pack()
    city_entry = Entry(root)
    city_entry.pack()

    Label(root, text="Deposit").pack()
    deposit_entry = Entry(root)
    deposit_entry.pack()

    Label(root, text="Password").pack()
    password_entry = Entry(root, show="*")
    password_entry.pack()


    def submit_new_user():
        name = name_entry.get()
        contact = contact_entry.get()
        dob = dob_entry.get()
        unique_id = unique_id_entry.get()
        city = city_entry.get()
        deposit = deposit_entry.get()
        password = password_entry.get()

        
        if not all([name, contact, dob, unique_id, city, deposit, password]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        
        c1.execute("SELECT * FROM user WHERE unique_id = %s OR contact = %s", (unique_id, contact))
        existing_user = c1.fetchone()
        if existing_user:
            messagebox.showerror("Error", "Account with this Unique ID or Contact already exists.")
        else:
            insertion = """INSERT INTO user(name, contact, dob, unique_id, city, deposit, password) 
                           VALUES(%s, %s, %s, %s, %s, %s, %s)"""
            c1.execute(insertion, (name, contact, dob, unique_id, city, deposit, password))
            conn.commit()
            messagebox.showinfo("Success", "New account created successfully!")
            main_menu()

    Button(root, text="Submit", command=submit_new_user).pack(pady=10)

    Button(root, text="Previous Page", command= main_menu).pack(pady=15)


def login_form():
    
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text="Enter Login Details").pack(pady=5)

    Label(root, text="Unique ID").pack()
    unique_id_entry = Entry(root)
    unique_id_entry.pack()

    Label(root, text="Password").pack()
    password_entry = Entry(root, show="*")
    password_entry.pack()

    def submit_login():
        unique_id = unique_id_entry.get()
        password = password_entry.get()

        c1.execute("SELECT * FROM user WHERE unique_id = %s AND password = %s", (unique_id, password))
        user = c1.fetchone()
        if user:
            messagebox.showinfo("Welcome", f"Welcome {user[0]}!")
            after_login()
        else:
            messagebox.showerror("Error", "No such user found. Please try again.")
            login_form()

    Button(root, text="Login", command=submit_login).pack(pady=10)
    Button(root, text="Previous Page", command= main_menu).pack(pady=12)


def after_login():
    
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text="Select Operation").pack(pady=5)

    Button(root, text="Fetch Bank Details", command=fetch_bank_details).pack(pady=5)
    Button(root, text="Transfer Money", command=transfer_money_form).pack(pady=5)
    Button(root, text="Previous Page", command= main_menu).pack(pady=15)


def fetch_bank_details():
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text="Enter Details to Fetch").pack(pady=5)

    Label(root, text="Unique ID").pack()
    unique_id_entry = Entry(root)
    unique_id_entry.pack()

    def fetch_details():
        unique_id = unique_id_entry.get()
        c1.execute("SELECT name, deposit FROM user WHERE unique_id = %s", (unique_id,))
        user = c1.fetchone()
        if user:
            messagebox.showinfo("Details", f"Name: {user[0]}, Deposit: {user[1]}")
        else:
            messagebox.showerror("Error", "No such user found.")
    
    Button(root, text="Fetch", command=fetch_details).pack(pady=10)


def transfer_money_form():
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text="Enter Transfer Details").pack(pady=5)

    Label(root, text="From (Your ID)").pack()
    from_entry = Entry(root)
    from_entry.pack()

    Label(root, text="To (Recipient's ID)").pack()
    to_entry = Entry(root)
    to_entry.pack()

    Label(root, text="Amount").pack()
    amount_entry = Entry(root)
    amount_entry.pack()

    def transfer_money():
        from_user = from_entry.get()
        to_user = to_entry.get()
        amount = int(amount_entry.get())

        
        c1.execute("UPDATE user SET deposit = deposit - %s WHERE unique_id = %s", (amount, from_user))
        conn.commit()

        c1.execute("UPDATE user SET deposit = deposit + %s WHERE unique_id = %s", (amount, to_user))
        conn.commit()

        messagebox.showinfo("Success", f"Transferred {amount} to {to_user}.")

    Button(root, text="Transfer", command=transfer_money).pack(pady=10)


def main_menu():
    for widget in root.winfo_children():
        widget.destroy()
    if bg:
        background= Label(root,image=bg)
        background.place(x=1,y=1,relheight=1,relwidth=1)
    
    Label(root, text="WELCOME TO BANK MANAGEMENT SYSTEM", font=("Arial",12,'bold'),bg='lightblue').pack(pady=10)
    Label(root, text="Main Menu",font=('bold',15),).pack(pady=(15,12),anchor=W,fill=X)
    
    Button(root, text="Create New Account", command=new_user_form,font=('bold',15)).pack(pady=5)
    Button(root, text="Existing Account", command=login_form,font=('bold',15)).pack(pady=5)
    Button(root, text="Exit", command=root.destroy,font=('bold',15)).pack(pady=80)

main_menu()

root.mainloop()
