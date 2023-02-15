import setup.py
import tkinter as tk
import subprocess
import platform
from tkinter import Menu
import os
from tkinter import filedialog
import tkinter.messagebox

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
    except Exception as e:
        print("An error occurred:", e)
        
def install_command():
    result = tkinter.messagebox.askyesno("Confirm", "Are you sure you want to install?")
    if result == True:
        install_command = "curl https://raw.githubusercontent.com/maidsafe/safe_network/master/resources/scripts/install.sh | bash"
        try:
            subprocess.run(install_command, shell=True,)
            output_box.config(state="normal")
            output_box.delete("1.0", tk.END)
            output_box.insert("1.0", "SAFE install complete, you can now join a network by entering the network name in the text box above and hitting join network, for a local network such as Baby-Fleming you are good to go!")
            output_box.config(state="disabled")
        except Exception as e:
            print("An error occurred:", e)
            
def join_command():
    testnet_name = command_entry.get()
    try:
        if testnet_name == "comnet":
            join_command = "safe networks add comnet https://sn-comnet.s3.eu-west-2.amazonaws.com/testnet_tool/comnet/network-contacts && safe networks switch comnet"
            print(f"Running command: {join_command}")
            result = subprocess.run(join_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output_box.config(state="normal")
            output_box.delete("1.0", tk.END)
            if "Error:" in result.stderr:
                output_box.insert("1.0", result.stderr)
            else:
                output_box.insert("1.0", "You have joined the Comnet Network!")
            output_box.config(state="disabled")
        else:
            join_command = f"safe networks add {testnet_name} https://sn-node.s3.eu-west-2.amazonaws.com/testnet_tool/{testnet_name}/network-contacts && safe networks switch {testnet_name}"
            print(f"Running command: {join_command}")
            result = subprocess.run(join_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output_box.config(state="normal")
            output_box.delete("1.0", tk.END)
            if "Error:" in result.stderr:
                output_box.insert("1.0", result.stderr)
            else:
                output_box.insert("1.0", f"You have joined the {testnet_name} network!")
            output_box.config(state="disabled")
    except Exception as e:
        print(f"Failed: {e}")
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", "Error:\n 0: 403 Failed to fetch network map")
        output_box.config(state="disabled")     

def container_command():
    command = command_entry.get()
    if "safe://" in command:
        container_command = "safe files ls " + command
        try:
            result = subprocess.run(container_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output_box.config(state="normal")
            output_box.delete("1.0", tk.END)
            output_box.insert("1.0", result.stdout)
        except Exception as e:
            print("An error occurred:", e)
            output_box.config(state="normal")
            output_box.delete("1.0", tk.END)
            output_box.insert("1.0", "Error:\n" + str(e))
        output_box.config(state="disabled")
    else:
        print("Input must contain 'safe://'")
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", "Error:\nInput must contain 'safe://'")
        output_box.config(state="disabled")

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
root.geometry("800x625")
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


command_entry = tk.Entry(root, width=80, font=("TkDefaultFont", 10))
command_entry.grid(row=1, column=1, pady=10, columnspan=3)
command_entry.config(fg='#666060')
#command_entry.insert(0, 'safe://hy8oyeyybwsanc3ehnecyab9n3ufoip6x47e6553rb539aeqnej1xwadcbfdo')
command_entry.bind("<Return>", run_command)
command_entry.bind("<Button-3>", right_click_event)


browse_button = tk.Button(root, text="Select File", bd=1, font=("Verdana", 10, "italic"), command=browse_file)
browse_button.grid(row=2, column=2, pady=10)

safe_command = tk.Button(root, text="View", command=run_command, bd=0, font=("Verdana", 12, "bold"))
safe_command.grid(row=2, column=1)

safe_put_command = tk.Button(root, text="Upload", command=run_put_command, bd=0, font=("Verdana", 12, "bold"))
safe_put_command.grid(row=2, column=3)

clear_button = tk.Button(root, text="x", command=clear_command, relief=tk.SUNKEN, bd=0)
clear_button.grid(row=1, column=4, pady=0)

output_box = tk.Text(root, height=10, width=80)
output_box.grid(row=4, column=1, pady=10, columnspan=3)
output_box.config(state="disabled")
output_box.config(state="normal", font=("Arial", 10, "normal"))

install_button = tk.Button(root, text="Install", command=install_command, bd=0, font=("Verdana", 10, "bold"))
install_button.grid(row=6, column=1)

join_button = tk.Button(root, text="Join Network", command=join_command, bd=0, font=("Verdana", 10, "bold"))
join_button.grid(row=6, column=2)

container_button = tk.Button(root, text="Container Ls", command=container_command, bd=0, font=("Verdana", 10, "bold"))
container_button.grid(row=6, column=3)

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=4, column=4, pady=10)
output_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output_box.yview)

menu = Menu(output_box, tearoff=0)
menu.add_command(label="Copy", command=lambda: copy_text(None))

output_box.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))

root.mainloop()
