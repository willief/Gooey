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
    put_command = command_entry.get()
    safe_put_command = "safe files put " + put_command
    result = subprocess.run(safe_put_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert("1.0", result.stdout)
    output_box.config(state="disabled")

def browse_file():
    file_path = filedialog.askopenfilename()
    command_entry.delete(0, tk.END)
    command_entry.insert(0, file_path)

root = tk.Tk()
root.geometry("900x600")
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

browse_button = tk.Button(root, text="Files To Put", font=("Verdana", 10, "italic"), command=browse_file)
browse_button.grid(row=2, column=2, pady=10)


safe_command = tk.Button(root, text="Get", command=run_command, font=("Verdana", 12, "bold"))
safe_command.grid(row=2, column=1)


safe_put_command = tk.Button(root, text="Put", command=run_put_command, font=("Verdana", 12, "bold"))
safe_put_command.grid(row=2, column=3)

output_box = tk.Text(root, height=10, width=80)
output_box.grid(row=4, column=1, pady=10, columnspan=3)
output_box.config(state="disabled")

root.mainloop()
