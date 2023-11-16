import tkinter as tk
from tkinter import filedialog, simpledialog
import subprocess
import os

command_history = []

selected_folder_path = ""
selected_file_path = ""

current_directory_label = None

def execute_command(command):
    if selected_folder_path:
        command = command.replace("{folder_path}", selected_folder_path)
    if selected_file_path:
        command = command.replace("{file_path}", selected_file_path)
    try:
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)

        command_history.append(command)
        update_command_history()

        command_entry.delete(0, tk.END)

      
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, result)
        output_text.config(state=tk.DISABLED)
    except subprocess.CalledProcessError as e:
        result = f"Error: {e.output}"

     
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, result)
        output_text.config(state=tk.DISABLED)

    print(result)

def update_command_history():
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)
    for command in command_history:
        history_text.insert(tk.END, command + "\n")
    history_text.config(state=tk.DISABLED)

def on_enter(event):
    execute_command(command_entry.get())

def browse_folder():
    global selected_folder_path, current_directory_label

    folder_path = filedialog.askdirectory()

    if folder_path:
        selected_folder_path = folder_path
        folder_path_label.config(text="Selected Folder Path: " + selected_folder_path)

        

        if current_directory_label is None:
            current_directory_label = tk.Label(root, text="Current Working Directory: " + os.getcwd(), bg=bg_color, fg=fg_color)
            current_directory_label.pack()
        else:
            current_directory_label.config(text="Current Working Directory: " + os.getcwd())

        try:
            os.chdir(selected_folder_path)
        except OSError as e:
            current_directory_label.config(text="Error: " + str(e))

def select_file():
    global selected_file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        selected_file_path = file_path

def run_language(language):
    select_file()
    if selected_file_path:
        if language == "Python":
            execute_command(f'python "{selected_file_path}"')
        elif language == "C":
            execute_command(f"gcc {selected_file_path} -o {selected_file_path}.exe && {selected_file_path}.exe")
        elif language == "C++":
            execute_command(f"g++ {selected_file_path} -o {selected_file_path}.exe && {selected_file_path}.exe")
        elif language == "Java":
            execute_command(f'javac "{selected_file_path}"')
            class_name = os.path.basename(selected_file_path).split('.')[0]
            execute_command(f'java "{class_name}"')

def execute_git_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)

        command_history.append(command)
        update_command_history()

        command_entry.delete(0, tk.END)
        print(result)
    except subprocess.CalledProcessError as e:
        result = f"Error: {e.output}"
        print(result)

def push_changes():
    try:
        remote_url = subprocess.check_output("git config --get remote.origin.url", shell=True, text=True)
        if remote_url.strip():
            execute_git_command("git push -u origin main")
        else:
            remote_url = simpledialog.askstring("Remote URL", "Enter the Git remote URL:")
            if remote_url:
                execute_git_command(f"git remote add origin {remote_url}")
                execute_git_command("git push -u origin main")
    except subprocess.CalledProcessError as e:
        result = f"Error: {e.output}"
        print(result)

def commit_changes():
    commit_message = simpledialog.askstring("Commit Message", "Enter your commit message:")
    if commit_message is not None:
        execute_git_command(f'git commit -m "{commit_message}"')

root = tk.Tk()
root.title("Command Line GUI")

bg_color = "#2E2E2E"
fg_color = "#FFFFFF"
entry_bg_color = "#3E3E3E"
button_bg_color = "#4E4E4E"
title_color = "#FFA500"

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
git_menu.add_command(label="Push to Remote", command=push_changes)
git_menu.add_command(label="Pull from Remote", command=lambda: execute_git_command("git pull"))

run_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Run", menu=run_menu)
run_menu.add_command(label="Python", command=lambda: run_language("Python"))
run_menu.add_command(label="C", command=lambda: run_language("C"))
run_menu.add_command(label="C++", command=lambda: run_language("C++"))
run_menu.add_command(label="Java", command=lambda: run_language("Java"))

folder_path_label = tk.Label(root, text="Selected Folder Path: " + selected_folder_path, bg=bg_color, fg=fg_color)

folder_path_label.pack()

browse_folder_button = tk.Button(root, text="Browse Folder", command=browse_folder, bg=button_bg_color, fg=fg_color)
browse_folder_button.pack()

command_label = tk.Label(root, text="Enter a command:", bg=bg_color, fg=fg_color)
command_label.pack()
command_entry = tk.Entry(root, width=40, bg=entry_bg_color, fg=fg_color)
command_entry.pack(pady=5)

command_entry.bind("<Return>", on_enter)

execute_button = tk.Button(root, text="Execute", command=lambda: execute_command(command_entry.get()), bg=button_bg_color, fg=fg_color)
execute_button.pack()

history_label = tk.Label(root, text="Command History:", bg=bg_color, fg=fg_color)
history_label.pack()
history_text = tk.Text(root, height=10, width=50, state=tk.DISABLED, bg=bg_color, fg=fg_color)
history_text.pack()


output_text = tk.Text(root, height=10, width=50, state=tk.DISABLED, bg=bg_color, fg=fg_color)
output_text.pack()

update_command_history()


root.mainloop()
