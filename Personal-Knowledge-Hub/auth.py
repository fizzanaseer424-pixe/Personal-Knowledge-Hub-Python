import tkinter as tk
from tkinter import messagebox
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
# Register new user
def register_user():
    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields are required.")
        return

    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful! You can now log in.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists. Choose another one.")
    conn.close()
# Login existing user
def login_user():
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Success", f"Welcome, {username}!")
        root.destroy()
        # You can import and open your main app window here
        # e.g., from main import open_main_app
    else:
        messagebox.showerror("Error", "Invalid username or password.")
# GUI Layout
init_db()

root = tk.Tk()
root.title("Personal Knowledge Hub - Login/Register")
root.geometry("400x250")
root.resizable(False, False)

label_title = tk.Label(root, text="Login / Register", font=("Arial", 16))
label_title.pack(pady=10)

label_username = tk.Label(root, text="Username:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

btn_login = tk.Button(root, text="Login", width=15, command=login_user)
btn_login.pack(pady=5)

btn_register = tk.Button(root, text="Register", width=15, command=register_user)
btn_register.pack(pady=5)

root.mainloop()
