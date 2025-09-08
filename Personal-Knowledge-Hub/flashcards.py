import tkinter as tk
from tkinter import messagebox
import sqlite3

# -----------------------------
# Initialize database for flashcards
# -----------------------------
def init_db():
    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# -----------------------------
# Add new flashcard
# -----------------------------
def add_flashcard():
    question = entry_question.get()
    answer = entry_answer.get()

    if question == "" or answer == "":
        messagebox.showerror("Error", "Both question and answer are required.")
        return

    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO flashcards (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Flashcard added successfully!")
    entry_question.delete(0, tk.END)
    entry_answer.delete(0, tk.END)
    load_flashcards()

# -----------------------------
# Load all flashcards
# -----------------------------
def load_flashcards():
    global flashcards, current_index
    conn = sqlite3.connect("personal_knowledge_hub.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, answer FROM flashcards")
    flashcards = cursor.fetchall()
    conn.close()
    current_index = 0
    show_flashcard()

# -----------------------------
# Show current flashcard
# -----------------------------
def show_flashcard():
    if flashcards:
        lbl_flashcard.config(text=flashcards[current_index][1])
        btn_flip.config(state=tk.NORMAL)
        btn_delete.config(state=tk.NORMAL)
    else:
        lbl_flashcard.config(text="No flashcards found.")
        btn_flip.config(state=tk.DISABLED)
        btn_delete.config(state=tk.DISABLED)

# -----------------------------
# Flip flashcard
# -----------------------------
def flip_flashcard():
    if flashcards:
        current = lbl_flashcard.cget("text")
        if current == flashcards[current_index][1]:
            lbl_flashcard.config(text=flashcards[current_index][2])  # Show answer
        else:
            lbl_flashcard.config(text=flashcards[current_index][1])  # Show question

# -----------------------------
# Next flashcard
# -----------------------------
def next_flashcard():
    global current_index
    if flashcards:
        current_index = (current_index + 1) % len(flashcards)
        show_flashcard()

# -----------------------------
# Previous flashcard
# -----------------------------
def previous_flashcard():
    global current_index
    if flashcards:
        current_index = (current_index - 1) % len(flashcards)
        show_flashcard()

# -----------------------------
# Delete current flashcard
# -----------------------------
def delete_flashcard():
    if flashcards:
        confirm = messagebox.askyesno("Confirm", "Delete this flashcard?")
        if confirm:
            flashcard_id = flashcards[current_index][0]
            conn = sqlite3.connect("personal_knowledge_hub.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM flashcards WHERE id = ?", (flashcard_id,))
            conn.commit()
            conn.close()
            load_flashcards()

# -----------------------------
# GUI Layout
# -----------------------------
init_db()
flashcards = []
current_index = 0

root = tk.Tk()
root.title("Personal Knowledge Hub - Flashcards")
root.geometry("500x400")

# Add flashcard
frame_add = tk.Frame(root)
frame_add.pack(pady=10)

tk.Label(frame_add, text="Question:").grid(row=0, column=0, sticky="w")
entry_question = tk.Entry(frame_add, width=50)
entry_question.grid(row=0, column=1)

tk.Label(frame_add, text="Answer:").grid(row=1, column=0, sticky="w")
entry_answer = tk.Entry(frame_add, width=50)
entry_answer.grid(row=1, column=1)

btn_add = tk.Button(frame_add, text="Add Flashcard", command=add_flashcard)
btn_add.grid(row=2, column=0, columnspan=2, pady=5)

# Flashcard display
lbl_flashcard = tk.Label(root, text="No flashcards found.", font=("Arial", 16), wraplength=400, relief=tk.RIDGE, width=50, height=5)
lbl_flashcard.pack(pady=20)

frame_controls = tk.Frame(root)
frame_controls.pack()

btn_previous = tk.Button(frame_controls, text="Previous", command=previous_flashcard)
btn_previous.grid(row=0, column=0, padx=5)

btn_flip = tk.Button(frame_controls, text="Flip", command=flip_flashcard, state=tk.DISABLED)
btn_flip.grid(row=0, column=1, padx=5)

btn_next = tk.Button(frame_controls, text="Next", command=next_flashcard)
btn_next.grid(row=0, column=2, padx=5)

btn_delete = tk.Button(root, text="Delete Flashcard", command=delete_flashcard, state=tk.DISABLED)
btn_delete.pack(pady=10)

load_flashcards()
root.mainloop()
