import tkinter as tk
from tkinter import filedialog, simpledialog  # Import the necessary module for the commit message dialog
import subprocess
import os

command_history = []

selected_folder_path = ""

current_directory_label = None

def execute_command():      
    command = command_entry.get()
    if selected_folder_path:
        command = command.replace("{folder_path}", selected_folder_path)
    try:
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)

   
        command_history.append(command)
        update_command_history()

       
        command_entry.delete(0, tk.END)
    except subprocess.CalledProcessError as e:
       
        result = f"Error: {e.output}"

   
    print(result)

def update_command_history():
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)  
    for command in command_history:
        history_text.insert(tk.END, command + "\n")
    history_text.config(state=tk.DISABLED)

def on_enter(event):
    execute_command()

def browse_folder():
    global selected_folder_path, current_directory_label  
    folder_path = filedialog.askdirectory()
    if folder_path:
        selected_folder_path = folder_path
        folder_path_label.config(text="Selected Folder Path: " + selected_folder_path)
        try:
            os.chdir(selected_folder_path)
            current_directory_label.config(text="Current Working Directory: " + os.getcwd())
        except OSError as e:
            current_directory_label.config(text="Error: " + str(e))

def execute_git_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)

        # Append the executed Git command to the history
        command_history.append(command)
        update_command_history()

       
        command_entry.delete(0, tk.END)
    except subprocess.CalledProcessError as e:
      
        result = f"Error: {e.output}"

    print(result)


def commit_changes():
    commit_message = simpledialog.askstring("Commit Message", "Enter your commit message:")
    if commit_message is not None:
        execute_git_command(f'git commit -m "{commit_message}"')


root = tk.Tk()
root.title("Command Line GUI")


bg_color = "#2E2E2E"  # Dark gray background
fg_color = "#FFFFFF"  # White text
entry_bg_color = "#3E3E3E"  # Slightly lighter background for entry widget
button_bg_color = "#4E4E4E"  # Slightly lighter background for button widget
title_color = "#FFA500"  # Orange title color


root.configure(bg=bg_color)


title_bar = tk.Label(root, text="Commando", bg=bg_color, fg=title_color)
title_bar.pack()

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)


file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_command(label="Delete")   
git_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Git", menu=git_menu)
git_menu.add_command(label="Initialize Git Repository", command=lambda: execute_git_command("git init"))
git_menu.add_command(label="Add Files to Staging", command=lambda: execute_git_command("git add ."))
git_menu.add_command(label="Commit Changes", command=commit_changes)
git_menu.add_command(label="Push to Remote", command=lambda: execute_git_command("git push -u origin main"))
git_menu.add_command(label="Pull from Remote", command=lambda: execute_git_command("git pull"))
run_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Python")
run_menu.add_command(label="C")
run_menu.add_command(label="C++")
run_menu.add_command(label="Java")


folder_path_label = tk.Label(root, text="Selected Folder Path: " + selected_folder_path, bg=bg_color, fg=fg_color)
folder_path_label.pack()


browse_folder_button = tk.Button(root, text="Browse Folder", command=browse_folder, bg=button_bg_color, fg=fg_color)
browse_folder_button.pack()


command_label = tk.Label(root, text="Enter a command:", bg=bg_color, fg=fg_color)
command_label.pack()
command_entry = tk.Entry(root, width=40, bg=entry_bg_color, fg=fg_color)
command_entry.pack(pady=5)


command_entry.bind("<Return>", on_enter)


execute_button = tk.Button(root, text="Execute", command=execute_command, bg=button_bg_color, fg=fg_color)
execute_button.pack()


history_label = tk.Label(root, text="Command History:", bg=bg_color, fg=fg_color)
history_label.pack()
history_text = tk.Text(root, height=10, width=50, state=tk.DISABLED, bg=bg_color, fg=fg_color)
history_text.pack()


update_command_history()


root.mainloop()
