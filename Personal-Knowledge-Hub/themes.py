import tkinter as tk
from tkinter import ttk

def apply_light_theme(root):
    """
    Apply a light theme: light background, black text.
    Call this once in each module after creating your Tk() root window.
    """
    # Colors
    bg_color = "#f9f9f9"   # light background
    fg_color = "#000000"   # black text
    entry_bg = "#ffffff"   # white for entry fields
    button_bg = "#e6e6e6"  # light grey for buttons
    button_hover = "#cccccc"

    # Root window
    root.configure(bg=bg_color)

    # Use default ttk theme
    style = ttk.Style(root)
    style.theme_use('default')

    # General style for all widgets
    style.configure(
        ".",  # base
        background=bg_color,
        foreground=fg_color,
        font=("Arial", 11)
    )

    # Buttons
    style.configure(
        "TButton",
        background=button_bg,
        foreground=fg_color,
        borderwidth=1,
        focusthickness=3,
        focuscolor='none',
        padding=6
    )
    style.map(
        "TButton",
        background=[
            ("active", button_hover),
            ("pressed", button_hover)
        ]
    )

    # Labels
    style.configure(
        "TLabel",
        background=bg_color,
        foreground=fg_color
    )

    # Entry fields
    style.configure(
        "TEntry",
        fieldbackground=entry_bg,
        foreground=fg_color
    )

    # Frames
    style.configure(
        "TFrame",
        background=bg_color
    )

    # Progressbar
    style.configure(
        "TProgressbar",
        troughcolor="#e0e0e0",
        background="#007acc"
    )
