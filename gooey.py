import tkinter as tk
import subprocess
import os
from tkinter import filedialog

def run_command(*args):
    command = command_entry.get()
    safe_command = "safe cat " + command + " > download"
    subprocess.run(safe_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.system("open download")

def run_put_command(*args):
    put_command = put_command_entry.get()
    safe_put_command = "safe files put " + put_command
    result = subprocess.run(safe_put_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert("1.0", result.stdout)
    output_box.config(state="disabled")

def clear_command():
    command_entry.delete(0, tk.END)

def clear_put_command():
    put_command_entry.delete(0, tk.END)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")

def browse_file():
    file_path = filedialog.askopenfilename()
    put_command_entry.delete(0, tk.END)
    put_command_entry.insert(0, file_path)

root = tk.Tk()
root.title("Safe Gooey")
# root.config(bg='#454e52')
# root['bg'] = '#394245'
root.option_add("*Font", "Verdana 15 bold")


command_label = tk.Label(root, text="Enter XorUrl:")
command_label.pack(pady=10)

command_entry = tk.Entry(root, width=80)
command_entry.pack(pady=10)
command_entry.bind("<Return>", run_command)

run_button = tk.Button(root, text="GET", command=run_command)
run_button.pack(pady=10)

clear_button = tk.Button(root, text="Clear", command=clear_command)
clear_button.pack(pady=10)

put_command_label = tk.Label(root, text="PUT Files:")
put_command_label.pack(pady=10)

put_command_entry = tk.Entry(root, width=80)
put_command_entry.pack(pady=10)
put_command_entry.bind("<Return>", run_put_command)

run_put_button = tk.Button(root, text="PUT", command=run_put_command)
run_put_button.pack(pady=10)

clear_put_button = tk.Button(root, text="Clear PUT", command=clear_put_command)
clear_put_button.pack(pady=10)

browse_button = tk.Button(root, text="Browse Files", command=browse_file)
browse_button.pack(pady=10)

output_box = tk.Text(root, height=10, width=80)
output_box.pack(pady=10)
output_box.config(state="disabled")


root.mainloop()


