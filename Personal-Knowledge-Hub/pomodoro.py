import tkinter as tk
from tkinter import messagebox


# Timer settings (Pomodoro: 25 min, Short Break: 5 min)

WORK_MIN = 25
BREAK_MIN = 5


# Timer variables

timer_running = False
paused = False
remaining_time = 0
timer_id = None


# Start work session

def start_work():
    global remaining_time, timer_running, paused
    if timer_running:
        messagebox.showinfo("Running", "Timer is already running.")
        return
    remaining_time = WORK_MIN * 60
    timer_running = True
    paused = False
    update_timer()


# Start short break

def start_break():
    global remaining_time, timer_running, paused
    if timer_running:
        messagebox.showinfo("Running", "Timer is already running.")
        return
    remaining_time = BREAK_MIN * 60
    timer_running = True
    paused = False
    update_timer()


# Pause timer

def pause_timer():
    global paused, timer_running
    if not timer_running:
        return
    paused = True


# Resume timer

def resume_timer():
    global paused
    if not timer_running:
        return
    if not paused:
        return
    paused = False
    update_timer()


# Reset timer

def reset_timer():
    global timer_running, paused, remaining_time
    if timer_running:
        root.after_cancel(timer_id)
    timer_running = False
    paused = False
    remaining_time = 0
    label_timer.config(text="00:00")


# Update timer every second

def update_timer():
    global remaining_time, timer_id, timer_running
    if paused:
        return

    mins, secs = divmod(remaining_time, 60)
    time_format = '{:02d}:{:02d}'.format(mins, secs)
    label_timer.config(text=time_format)

    if remaining_time > 0:
        remaining_time -= 1
        timer_id = root.after(1000, update_timer)
    else:
        messagebox.showinfo("Time's up!", "Session complete!")
        timer_running = False


# GUI Layout

root = tk.Tk()
root.title("Personal Knowledge Hub - Pomodoro Timer")
root.geometry("300x250")
root.resizable(False, False)

label_title = tk.Label(root, text="Pomodoro Timer", font=("Arial", 16))
label_title.pack(pady=10)

label_timer = tk.Label(root, text="00:00", font=("Arial", 48))
label_timer.pack(pady=10)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_work = tk.Button(frame_buttons, text="Start Work", command=start_work, width=12)
btn_work.grid(row=0, column=0, padx=5)

btn_break = tk.Button(frame_buttons, text="Short Break", command=start_break, width=12)
btn_break.grid(row=0, column=1, padx=5)

btn_pause = tk.Button(frame_buttons, text="Pause", command=pause_timer, width=12)
btn_pause.grid(row=1, column=0, padx=5, pady=5)

btn_resume = tk.Button(frame_buttons, text="Resume", command=resume_timer, width=12)
btn_resume.grid(row=1, column=1, padx=5, pady=5)

btn_reset = tk.Button(root, text="Reset", command=reset_timer, width=26)
btn_reset.pack(pady=5)

root.mainloop()
