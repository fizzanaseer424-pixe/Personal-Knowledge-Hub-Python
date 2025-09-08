import tkinter as tk
from tkinter import ttk
import sqlite3


# Get stats from database

def get_stats():
    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()

    # To-Do stats
    cursor.execute("SELECT COUNT(*) FROM todo")
    total_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM todo WHERE done = 1")
    done_tasks = cursor.fetchone()[0]

    # Notes stats
    cursor.execute("SELECT COUNT(*) FROM notes")
    total_notes = cursor.fetchone()[0]

    # Flashcards stats
    cursor.execute("SELECT COUNT(*) FROM flashcards")
    total_flashcards = cursor.fetchone()[0]

    # Journal entries stats
    cursor.execute("SELECT COUNT(*) FROM journal")
    total_journal = cursor.fetchone()[0]

    conn.close()

    return total_tasks, done_tasks, total_notes, total_flashcards, total_journal

# -----------------------------
# Refresh progress stats
# -----------------------------
def refresh_stats():
    total_tasks, done_tasks, total_notes, total_flashcards, total_journal = get_stats()

    lbl_tasks.config(text=f"To-Do Tasks: {done_tasks}/{total_tasks}")
    lbl_notes.config(text=f"Notes: {total_notes}")
    lbl_flashcards.config(text=f"Flashcards: {total_flashcards}")
    lbl_journal.config(text=f"Journal Entries: {total_journal}")

    # Progress %
    if total_tasks == 0:
        percent = 0
    else:
        percent = int((done_tasks / total_tasks) * 100)

    progress_bar['value'] = percent
    lbl_progress.config(text=f"Tasks Completion: {percent}%")

# -----------------------------
# GUI Layout
# -----------------------------
root = tk.Tk()
root.title("Personal Knowledge Hub - Progress Tracker")
root.geometry("400x300")
root.resizable(False, False)

label_title = tk.Label(root, text="Your Progress Overview", font=("Arial", 16))
label_title.pack(pady=10)

lbl_tasks = tk.Label(root, text="To-Do Tasks: 0/0", font=("Arial", 12))
lbl_tasks.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)

lbl_progress = tk.Label(root, text="Tasks Completion: 0%", font=("Arial", 12))
lbl_progress.pack(pady=5)

lbl_notes = tk.Label(root, text="Notes: 0", font=("Arial", 12))
lbl_notes.pack(pady=5)

lbl_flashcards = tk.Label(root, text="Flashcards: 0", font=("Arial", 12))
lbl_flashcards.pack(pady=5)

lbl_journal = tk.Label(root, text="Journal Entries: 0", font=("Arial", 12))
lbl_journal.pack(pady=5)

btn_refresh = tk.Button(root, text="Refresh", command=refresh_stats, width=20)
btn_refresh.pack(pady=10)

# Load initial stats
refresh_stats()

root.mainloop()
