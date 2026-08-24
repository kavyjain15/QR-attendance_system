import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_PATH = "database/qr_attendance.db"

def check_login(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM teachers WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()
    return user

def login():
    email = entry_email.get()
    password = entry_password.get()

    user = check_login(email, password)
    if user:
        messagebox.showinfo("Login Success", f"Welcome {user[1]}!")  
        root.destroy()
        import main  # ✅ this will open your main attendance system
    else:
        messagebox.showerror("Error", "Invalid Email or Password")

# --- GUI ---
root = tk.Tk()
root.title("Teacher Login")
root.geometry("300x200")

tk.Label(root, text="Email:").pack(pady=5)
entry_email = tk.Entry(root)
entry_email.pack()

tk.Label(root, text="Password:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()
