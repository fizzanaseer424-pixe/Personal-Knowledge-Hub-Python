import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3


# Initialize database for notes

def init_db():
    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()


# Add new note

def add_note():
    title = entry_title.get()
    content = text_content.get("1.0", tk.END).strip()

    if title == "" or content == "":
        messagebox.showerror("Error", "Both title and content are required.")
        return

    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Note added successfully!")
    entry_title.delete(0, tk.END)
    text_content.delete("1.0", tk.END)
    load_notes()


# Load notes to listbox

def load_notes():
    listbox_notes.delete(0, tk.END)
    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM notes")
    for note in cursor.fetchall():
        listbox_notes.insert(tk.END, f"{note[0]}. {note[1]}")
    conn.close()


# View selected note

def view_note():
    try:
        selection = listbox_notes.get(listbox_notes.curselection())
        note_id = int(selection.split(".")[0])
    except:
        messagebox.showerror("Error", "Please select a note to view.")
        return

    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    conn.close()

    if note:
        entry_title.delete(0, tk.END)
        entry_title.insert(0, note[0])
        text_content.delete("1.0", tk.END)
        text_content.insert(tk.END, note[1])


# Delete selected note

def delete_note():
    try:
        selection = listbox_notes.get(listbox_notes.curselection())
        note_id = int(selection.split(".")[0])
    except:
        messagebox.showerror("Error", "Please select a note to delete.")
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this note?")
    if confirm:
        conn = sqlite3.connect("personal_knowledge_hub.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Note deleted successfully!")
        entry_title.delete(0, tk.END)
        text_content.delete("1.0", tk.END)
        load_notes()


# Update selected note

def update_note():
    try:
        selection = listbox_notes.get(listbox_notes.curselection())
        note_id = int(selection.split(".")[0])
    except:
        messagebox.showerror("Error", "Please select a note to update.")
        return

    title = entry_title.get()
    content = text_content.get("1.0", tk.END).strip()

    if title == "" or content == "":
        messagebox.showerror("Error", "Both title and content are required.")
        return

    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, note_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Note updated successfully!")
    load_notes()


# GUI Layout

init_db()

root = tk.Tk()
root.title("Personal Knowledge Hub - Notes")
root.geometry("600x500")

frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Notes list
listbox_notes = tk.Listbox(frame_left, width=30)
listbox_notes.pack(fill=tk.Y)

btn_view = tk.Button(frame_left, text="View", command=view_note)
btn_view.pack(pady=5)

btn_delete = tk.Button(frame_left, text="Delete", command=delete_note)
btn_delete.pack(pady=5)

# Note details
label_title = tk.Label(frame_right, text="Title:")
label_title.pack()
entry_title = tk.Entry(frame_right, width=50)
entry_title.pack()

label_content = tk.Label(frame_right, text="Content:")
label_content.pack()
text_content = tk.Text(frame_right, width=50, height=20)
text_content.pack()

btn_add = tk.Button(frame_right, text="Add Note", command=add_note)

