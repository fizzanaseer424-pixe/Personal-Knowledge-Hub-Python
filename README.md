Personal Knowledge Hub
Overview

Personal Knowledge Hub is a beginner-friendly Python desktop application that helps students and professionals organize, manage, and track their learning in one place. It combines features such as note-taking, flashcards, to-do lists, journaling, progress tracking, and productivity tools, all powered by a lightweight SQLite database.

Features

The application includes an authentication system for user login, a notes module for creating and managing notes, a flashcards module for quick learning and revision, and a to-do list manager for organizing tasks and deadlines. It also offers a Pomodoro timer to improve productivity, a journal for daily reflections, and a progress tracker to monitor goals. In addition, users can apply custom themes, export and import their data for backup, and rely on a built-in SQLite database for local storage.

Project Structure

The project is organized into several Python modules. The auth.py file handles authentication, database.py manages the SQLite connection, and notes.py, flashcards.py, todo.py, journal.py, pomodoro.py, and progress.py implement the core features. themes.py allows customization of the interface, while export_import.py provides backup and restore functionality. The main user interface is handled by main_ui.py, and the application entry point is provided in main.py (originally included as main.py.txt). The project also contains a preconfigured SQLite database file named personal_knowledge_hub.db. A detailed user manual is available in the file DocumentationPersonalKnowledgeHub.docx.

Installation and Setup

To get started, clone the repository and navigate into the project directory. It is recommended to create a Python virtual environment. If a requirements.txt file is provided, install the dependencies using pip install -r requirements.txt. Next, rename main.py.txt to main.py and run the application with the command python main.py.

Documentation

Detailed usage instructions and explanations of each module are provided in the file DocumentationPersonalKnowledgeHub.docx.

Tech Stack

The application is built with Python 3.12 and makes use of Tkinter for the graphical user interface and SQLite for database storage.

Roadmap

Planned enhancements include cloud backup integration, an analytics dashboard to provide insights into learning patterns, and a mobile-friendly version of the application.

Author

This project was developed by Fizza Naseer.
