import tkinter as tk
import subprocess
import platform
from tkinter import Menu
import os
from tkinter import filedialog

def run_command(*args):
    command = command_entry.get()
    safe_command = "safe cat " + command + " > ~/Downloads/download"
    try:
        subprocess.run(safe_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if platform.system() == "Linux":
            os.system("xdg-open ~/Downloads/download")
        elif platform.system() == "Windows":
            os.startfile("~/Downloads/download")
        elif platform.system() == "Darwin":
            os.system("open ~/Downloads/download")
    except Exception as e:
        print("An error occurred:", e)

def run_put_command(*args):
    put_command = command_entry.get()
    safe_put_command = "safe files put " + put_command
    try:
        result = subprocess.run(safe_put_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", result.stdout)
        output_box.config(state="disabled")
    except Exception as e:
        print("An error occurred:", e)

def clear_command():
    command_entry.delete(0, tk.END)

def browse_file():
    file_path = filedialog.askopenfilename()
    command_entry.delete(0, tk.END)
    command_entry.insert(0, file_path)

def right_click_event(event):
    try:
        widget = event.widget
        widget.event_generate("<<Paste>>")
    except tk.TclError:
        pass

def copy_text(event):
    output_box.event_generate("<<Copy>>")
        
root = tk.Tk()
root.geometry("800x550")
root.resizable(False, False)
root.title("SAFE CLI GUI")
root.option_add("*Font", "Verdana 15")

root.columnconfigure(0, minsize=30, weight=1)
root.columnconfigure(1, minsize=30, weight=1)
root.columnconfigure(2, minsize=30, weight=1)
root.columnconfigure(3, minsize=30, weight=1)
root.columnconfigure(4, minsize=30, weight=1)

command_label = tk.Label(root, text="Gooey", font=("Product Sans", 20, "bold"), fg="#0b275b", justify="center")
command_label.grid(row=0, column=2, pady=50)


command_entry = tk.Entry(root, width=80)
command_entry.grid(row=1, column=1, pady=10, columnspan=3)
command_entry.bind("<Return>", run_command)
command_entry.bind("<Button-3>", right_click_event)


browse_button = tk.Button(root, text="Files To Put", bd=0, font=("Verdana", 10, "italic"), command=browse_file)
browse_button.grid(row=2, column=2, pady=10)

safe_command = tk.Button(root, text="Get", command=run_command, bd=0, font=("Verdana", 12, "bold"))
safe_command.grid(row=2, column=1)

safe_put_command = tk.Button(root, text="Put", command=run_put_command, bd=0, font=("Verdana", 12, "bold"))
safe_put_command.grid(row=2, column=3)

clear_button = tk.Button(root, text="x", command=clear_command, relief=tk.SUNKEN, bd=0)
clear_button.grid(row=1, column=4, pady=0)

output_box = tk.Text(root, height=10, width=80)
output_box.grid(row=4, column=1, pady=10, columnspan=3)
output_box.config(state="disabled")

menu = Menu(output_box, tearoff=0)
menu.add_command(label="Copy", command=lambda: copy_text(None))

output_box.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))

root.mainloop()
