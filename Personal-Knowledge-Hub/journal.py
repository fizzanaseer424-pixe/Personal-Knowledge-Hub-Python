import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import sqlite3
from datetime import datetime

# -----------------------------
# Initialize database for journal
# -----------------------------
def init_db():
    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# -----------------------------
# Add new journal entry
# -----------------------------
def add_entry():
    title = entry_title.get().strip()
    content = text_content.get("1.0", tk.END).strip()

    if title == "" or content == "":
        messagebox.showerror("Error", "Both title and content are required.")
        return

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO journal (date, title, content) VALUES (?, ?, ?)", (date, title, content))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Journal entry saved!")
    entry_title.delete(0, tk.END)
    text_content.delete("1.0", tk.END)
    load_entries()

# -----------------------------
# Load all entries
# -----------------------------
def load_entries():
    listbox_entries.delete(0, tk.END)
    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, title FROM journal ORDER BY date DESC")
    for entry in cursor.fetchall():
        listbox_entries.insert(tk.END, f"{entry[0]}. {entry[1][:10]} - {entry[2]}")
    conn.close()

# -----------------------------
# View selected entry
# -----------------------------
def view_entry():
    try:
        selection = listbox_entries.get(listbox_entries.curselection())
        entry_id = int(selection.split(".")[0])
    except:
        messagebox.showerror("Error", "Please select an entry to view.")
        return

    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, title, content FROM journal WHERE id = ?", (entry_id,))
    entry = cursor.fetchone()
    conn.close()

    if entry:
        entry_title.delete(0, tk.END)
        entry_title.insert(0, entry[1])
        text_content.delete("1.0", tk.END)
        text_content.insert(tk.END, entry[2])

# -----------------------------
# Delete selected entry
# -----------------------------
def delete_entry():
    try:
        selection = listbox_entries.get(listbox_entries.curselection())
        entry_id = int(selection.split(".")[0])
    except:
        messagebox.showerror("Error", "Please select an entry to delete.")
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this entry?")
    if confirm:
        conn = sqlite3.connect("personal_knowledge_hub.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM journal WHERE id = ?", (entry_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Journal entry deleted.")
        entry_title.delete(0, tk.END)
        text_content.delete("1.0", tk.END)
        load_entries()

# -----------------------------
# GUI Layout
# -----------------------------
init_db()

root = tk.Tk()
root.title("Personal Knowledge Hub - Journal")
root.geometry("700x500")

frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Journal entries list
listbox_entries = tk.Listbox(frame_left, width=40)
listbox_entries.pack(fill=tk.Y)

btn_view = tk.Button(frame_left, text="View Entry", command=view_entry)
btn_view.pack(pady=5)

btn_delete = tk.Button(frame_left, text="Delete Entry", command=delete_entry)
btn_delete.pack(pady=5)

# Entry details
label_title = tk.Label(frame_right, text="Title:")
label_title.pack(anchor="w")
entry_title = tk.Entry(frame_right, width=70)
entry_title.pack(fill=tk.X, pady=5)

label_content = tk.Label(frame_right, text="Content:")
label_content.pack(anchor="w")
text_content = tk.Text(frame_right, wrap=tk.WORD, width=70, height=20)
text_content.pack(fill=tk.BOTH, expand=True, pady=5)

btn_add = tk.Button(frame_right, text="Add Entry", command=add_entry)
btn_add.pack(pady=5)

load_entries()
root.mainloop()
