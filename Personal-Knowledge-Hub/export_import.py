import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import os


# Export data to SQL file

def export_data():
    filename = filedialog.asksaveasfilename(
        defaultextension=".sql",
        filetypes=[("SQL Files", "*.sql"), ("All Files", "*.*")]
    )
    if not filename:
        return

    try:
        conn = sqlite3.connect("personal_knowledge_hub.db")
        with open(filename, 'w', encoding='utf-8') as f:
            for line in conn.iterdump():
                f.write('%s\n' % line)
        conn.close()
        messagebox.showinfo("Export Successful", f"Data exported to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed.\n{str(e)}")

# -----------------------------
# Import data from SQL file
# -----------------------------
def import_data():
    filename = filedialog.askopenfilename(
        filetypes=[("SQL Files", "*.sql"), ("All Files", "*.*")]
    )
    if not filename:
        return

    confirm = messagebox.askyesno(
        "Confirm Import",
        "Importing will overwrite your existing data. Continue?"
    )
    if not confirm:
        return

    try:
        conn = sqlite3.connect("personal_knowledge_hub.db")
        cursor = conn.cursor()
        # Drop existing tables to avoid conflicts
        cursor.executescript("""
            DROP TABLE IF EXISTS todo;
            DROP TABLE IF EXISTS notes;
            DROP TABLE IF EXISTS flashcards;
            DROP TABLE IF EXISTS journal;
        """)
        # Execute SQL dump
        with open(filename, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        messagebox.showinfo("Import Successful", f"Data imported from {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Import failed.\n{str(e)}")

# -----------------------------
# GUI Layout
# -----------------------------
root = tk.Tk()
root.title("Personal Knowledge Hub - Export & Import")
root.geometry("400x200")
root.resizable(False, False)

label_title = tk.Label(root, text="Export & Import Data", font=("Arial", 16))
label_title.pack(pady=20)

btn_export = tk.Button(root, text="Export Data", command=export_data, width=30)
btn_export.pack(pady=10)

btn_import = tk.Button(root, text="Import Data", command=import_data, width=30)
btn_import.pack(pady=10)

root.mainloop()
