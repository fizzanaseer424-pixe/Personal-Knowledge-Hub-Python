import tkinter as tk
from tkinter import messagebox
import sqlite3

# -----------------------------
# Initialize database for To-Do
# -----------------------------
def init_db():
    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# -----------------------------
# Add new task
# -----------------------------
def add_task():
    task = entry_task.get().strip()
    if task == "":
        messagebox.showerror("Error", "Task cannot be empty.")
        return

    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todo (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()

    entry_task.delete(0, tk.END)
    load_tasks()

# -----------------------------
# Load tasks to listbox
# -----------------------------
def load_tasks():
    listbox_tasks.delete(0, tk.END)
    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, done FROM todo")
    for task in cursor.fetchall():
        status = "[✓] " if task[2] else "[ ] "
        listbox_tasks.insert(tk.END, f"{task[0]}. {status}{task[1]}")
    conn.close()

# -----------------------------
# Toggle task done/undone
# -----------------------------
def toggle_task():
    try:
        selection = listbox_tasks.get(listbox_tasks.curselection())
        task_id = int(selection.split(".")[0])
    except:
        messagebox.showerror("Error", "Please select a task to toggle.")
        return

    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT done FROM todo WHERE id = ?", (task_id,))
    done = cursor.fetchone()[0]
    new_done = 0 if done else 1
    cursor.execute("UPDATE todo SET done = ? WHERE id = ?", (new_done, task_id))
    conn.commit()
    conn.close()
    load_tasks()

# -----------------------------
# Delete task
# -----------------------------
def delete_task():
    try:
        selection = listbox_tasks.get(listbox_tasks.curselection())
        task_id = int(selection.split(".")[0])
    except:
        messagebox.showerror("Error", "Please select a task to delete.")
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this task?")
    if confirm:
        conn = sqlite3.connect("personal_knowledge_hub.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todo WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        load_tasks()

# -----------------------------
# GUI Layout
# -----------------------------
init_db()

root = tk.Tk()
root.title("Personal Knowledge Hub - To-Do List")
root.geometry("400x400")

label_task = tk.Label(root, text="Enter new task:")
label_task.pack(pady=5)

entry_task = tk.Entry(root, width=40)
entry_task.pack(pady=5)

btn_add = tk.Button(root, text="Add Task", command=add_task)
btn_add.pack(pady=5)

listbox_tasks = tk.Listbox(root, width=50)
listbox_tasks.pack(pady=10, fill=tk.BOTH, expand=True)

btn_toggle = tk.Button(root, text="Mark Done/Undone", command=toggle_task)
btn_toggle.pack(pady=5)

btn_delete = tk.Button(root, text="Delete Task", command=delete_task)
btn_delete.pack(pady=5)

load_tasks()
root.mainloop()
