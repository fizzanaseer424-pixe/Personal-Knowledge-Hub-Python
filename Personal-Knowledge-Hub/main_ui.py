import tkinter as tk
from tkinter import ttk
import subprocess
from themes import apply_light_theme

# -----------------------------
# Function to open modules
# -----------------------------
def open_module(module_name):
    try:
        subprocess.Popen(["python", f"{module_name}.py"])
    except Exception as e:
        print(f"Error opening {module_name}: {e}")

# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()
root.title("Personal Knowledge Hub - Dashboard")
root.geometry("400x500")
root.resizable(False, False)

apply_light_theme(root)

label_title = ttk.Label(root, text="Personal Knowledge Hub", font=("Arial", 18))
label_title.pack(pady=20)

# -----------------------------
# Module Buttons
# -----------------------------
modules = [
    ("Authentication", "auth"),
    ("Notes", "notes"),
    ("Flashcards", "flashcards"),
    ("To-Do List", "todo"),
    ("Journal", "journal"),
    ("Pomodoro Timer", "pomodoro"),
    ("Progress Tracker", "progress"),
    ("Export / Import", "export_import"),
]

for text, module in modules:
    btn = ttk.Button(root, text=text, command=lambda m=module: open_module(m), width=30)
    btn.pack(pady=8)

# Exit
btn_exit = ttk.Button(root, text="Exit", command=root.destroy, width=30)
btn_exit.pack(pady=20)

root.mainloop()
