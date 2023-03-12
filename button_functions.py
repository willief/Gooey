"""
Module containing functions to be executed on button click events.
"""

import os

import subprocess

import datetime

import tkinter

from tkinter import messagebox, simpledialog, filedialog

import shutil

import threading

import time

import webbrowser

import platform

from tqdm import tqdm

def install_safe(output_box):
    if os.path.exists("/usr/local/bin/safe"):
        safe_rm(output_box)

    result = messagebox.askyesno("Confirm", "Install SAFE?")
    if result is True:
        install_command = "curl https://raw.githubusercontent.com/maidsafe/safe_network/master/resources/scripts/install.sh | bash" 
        try:
            subprocess.run(install_command, shell=True, check=True)
            output_box.config(state="normal")
            output_box.delete("1.0", tkinter.END)
            output_box.insert("1.0", "SAFE install complete, you can now join a live network or to run a local network such as Baby-Fleming hit Install Node!")
            output_box.config(state="disabled")
        except subprocess.CalledProcessError as called_process_error:
            print("An error occurred:", called_process_error)

def install_node(output_box, root):
    result = tkinter.messagebox.askyesno("Confirm", "Install Node?")
    if result is True:
        output_box.config(state=tkinter.NORMAL)
        output_box.delete("1.0", tkinter.END)
        output_box.insert(tkinter.END, "Installing node...\n")
        output_box.config(state=tkinter.DISABLED)

        def install_safe_node():
            try:
                subprocess.check_output(["safe", "node", "install"], stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
            except subprocess.CalledProcessError as called_process_error:
                output_box.config(state=tkinter.NORMAL)
                output_box.insert(tkinter.END, called_process_error.output)
                output_box.config(state=tkinter.DISABLED)
                return

            output_box.config(state=tkinter.NORMAL)
            output_box.delete("1.0", tkinter.END)
            output_box.insert(tkinter.END, "Node successfully installed!\n")
            output_box.config(state=tkinter.DISABLED)

        def update_progress_bar():
            with tqdm(total=10) as progress_bar:
                while thread.is_alive():
                    progress_bar.update(1)
                    output_box.config(state=tkinter.NORMAL)
                    output_box.delete("1.0", tkinter.END)
                    output_box.insert(tkinter.END, f"Installing node{'.' * (int(progress_bar.n / 10) % 4)}\n")
                    output_box.config(state=tkinter.DISABLED)
                    root.update()
                    time.sleep(0.1)

        thread = threading.Thread(target=install_safe_node)
        thread.start()

        update_thread = threading.Thread(target=update_progress_bar)
        update_thread.start()

def node_join():
    pass

def safe_version(output_box):
    safe_path = shutil.which("safe")
    if safe_path is not None:
        command = [safe_path, "--version"]
        command2 = [safe_path, "node", "bin-version"]

        output_box.config(state=tkinter.NORMAL)

        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT)
            output_box.insert(tkinter.END, output.decode())

            output2 = subprocess.check_output(command2, stderr=subprocess.STDOUT)
            output2_str = output2.decode()
            output_box.insert(tkinter.END, output2_str)

            if "node not found" in output2_str:
                output_box.config(state=tkinter.NORMAL)
                output_box.delete("end-1l", tkinter.END)
                output_box.insert(tkinter.END, "Node not installed\n")
                output_box.config(state=tkinter.DISABLED)

        except subprocess.CalledProcessError as e:
            if "executable not found" in e.output.decode():
                output_box.insert(tkinter.END, "Node is not installed.\n")
            else:
                output_box.insert(tkinter.END, e.output.decode())

        output_box.config(state=tkinter.DISABLED)

    else:
        output_box.config(state=tkinter.NORMAL)
        output_box.insert(tkinter.END, "SAFE is not installed\n")
        output_box.config(state=tkinter.DISABLED)

def get_sudo_password():
    password = simpledialog.askstring("Password", "Please enter your password:", show="*")
    return password

def safe_rm(output_box):
    result = messagebox.askyesno("Confirm", "Remove existing SAFE?")
    if result:
        safe_path = "/usr/local/bin/safe"
        if os.path.exists(safe_path):
            password = simpledialog.askstring("Password", "Please enter your password:", show="*")
            if password:
                try:
                    subprocess.run(["sudo", "-S", "rm", "-rf", os.path.expanduser("~/.safe")], input=password.encode(), check=True)
                    subprocess.run(["sudo", "-S", "rm", safe_path], input=password.encode(), check=True) 
                    output_box.config(state="normal")
                    output_box.delete("1.0", tkinter.END)
                    output_box.insert("1.0", "You have successfully removed SAFE.")
                    output_box.config(state="disabled")
                except subprocess.CalledProcessError as e:
                    print("An error occurred:", e)
                    output_box.config(state="normal")
                    output_box.delete("1.0", tkinter.END)
                    output_box.insert("1.0", "Error removing SAFE.")
                    output_box.config(state="disabled")
            else:
                output_box.config(state="normal")
                output_box.delete("1.0", tkinter.END)
                output_box.insert("1.0", "Password is required.")
                output_box.config(state="disabled")
        else:
            try:
                subprocess.run(["rm", "-rf", os.path.expanduser("~/.safe")], check=True)
                output_box.config(state="normal")
                output_box.delete("1.0", tkinter.END)
                output_box.insert("1.0", "You have successfully removed SAFE.")
                output_box.config(state="disabled")
            except subprocess.CalledProcessError as e:
                print("An error occurred:", e)
                output_box.config(state="normal")
                output_box.delete("1.0", tkinter.END)
                output_box.insert("1.0", "Error removing SAFE.")
                output_box.config(state="disabled")
    else:
        output_box.config(state="normal")
        output_box.delete("1.0", tkinter.END)
        output_box.insert("1.0", "SAFE removal canceled.")
        output_box.config(state="disabled")

def jpl_primer():
    webbrowser.open_new("https://primer.safenetwork.org")

def about_info(output_box):
    message = "Gooey: SAFE Network CLI GUI.\n\n" \
              "Version 0.2.48\n\n" \
              "By @josh Safe Network Forum - @joshclsn Twitter.\n\n"\
              "Primer Courtesy @JPL Safe Network Forum."
    output_box.config(state=tkinter.NORMAL)
    output_box.delete("1.0", tkinter.END)
    output_box.insert(tkinter.END, message)
    output_box.config(state=tkinter.DISABLED)

def add_maidsafe(output_box, network_name=None):
    if network_name is None:
        network_name = tkinter.simpledialog.askstring("Enter Network Name", "Enter the network name:") 
        if network_name is None:
            return

    filename = os.path.join(os.path.expanduser("~/Gooey/.network_name.txt"))
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, "w", encoding="utf-8") as f:
        f.write(network_name)

    command = ["safe", "networks", "add", network_name, f"https://sn-node.s3.eu-west-2.amazonaws.com/testnet_tool/{network_name}/network-contacts"] 
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output_box.config(state=tkinter.NORMAL)
        output_box.insert(tkinter.END, f"You have added the {network_name} network.\n")
        output_box.config(state=tkinter.DISABLED)
    except subprocess.CalledProcessError as e:
        output_box.config(state=tkinter.NORMAL)
        output_box.insert(tkinter.END, f"Error adding the {network_name} network:\n{e.output.decode()}\n") 
        output_box.config(state=tkinter.DISABLED)

def get_network_name():
    file_path = os.path.expanduser("~/Gooey/.network_name.txt")
    if not os.path.isfile(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        network_name = f.read().strip()
    return network_name

def save_network_name(network_name):
    directory = os.path.expanduser("~/Gooey")
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, ".network_name.txt")
    if not os.path.exists(filename):
        open(filename, "w", encoding="utf-8").close()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(network_name)

def switch_maidsafe(output_box):
    network_name = get_network_name()
    if network_name is None:
        tkinter.messagebox.showerror("Error", "No network found. Please add a network first.")
        return

    command = ["safe", "networks", "switch", network_name]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output_box.config(state=tkinter.NORMAL)
        output_box.insert(tkinter.END, f"You have switched to the {network_name} network.\n")
        output_box.config(state=tkinter.DISABLED)
    except subprocess.CalledProcessError as e:
        output_box.config(state=tkinter.NORMAL)
        output_box.insert(tkinter.END, f"Error switching to the {network_name} network:\n{e.output.decode()}\n") 
        output_box.config(state=tkinter.DISABLED)

def add_comnet(output_box):
    command = ["safe", "networks", "add", "comnet", "https://sn-comnet.s3.eu-west-2.amazonaws.com/testnet_tool/comnet/network-contacts"] 
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        print(result)
        output_box.config(state=tkinter.NORMAL)
        output_box.insert(tkinter.END, "You have added the Comnet network.\n")
        output_box.config(state=tkinter.DISABLED)
    except subprocess.CalledProcessError as e:
        print(e.output.decode())
        output_box.config(state=tkinter.NORMAL)
        output_box.insert(tkinter.END, f"Error adding the Comnet network:\n{e.output.decode()}\n")
        output_box.config(state=tkinter.DISABLED)


def switch_comnet(output_box):
    try:
        output_box.config(state=tkinter.NORMAL)
        subprocess.check_output(["safe", "networks", "switch", "comnet"], stderr=subprocess.STDOUT)
        output_box.insert(tkinter.END, "You have switched to the Comnet network.\n")
    except subprocess.CalledProcessError as e:
        output_box.insert(tkinter.END, e.output.decode())
        output_box.insert(tkinter.END, "Error switching network to Comnet.\n")
    finally:
        output_box.config(state=tkinter.DISABLED)

def kill_node(output_box):
    try:
        subprocess.check_output(["pgrep", "sn_node"])
    except subprocess.CalledProcessError as e:
        output_box.config(state=tkinter.NORMAL)
        output_box.insert(tkinter.END, "Node not running\n")
        output_box.config(state=tkinter.DISABLED)
        return

    confirmed = messagebox.askyesno("Confirm", "Are you sure you want to kill your node?")
    if confirmed:
        try:
            output_box.config(state=tkinter.NORMAL)
            subprocess.check_output(["safe", "node", "killall"], stderr=subprocess.STDOUT)
            output_box.insert(tkinter.END, "Kill Success\n")
        except subprocess.CalledProcessError as e:
            output_box.insert(tkinter.END, e.output.decode())
            output_box.insert(tkinter.END, "Error killing node.\n")
        finally:
            output_box.config(state=tkinter.DISABLED)

def run_baby_fleming(output_box, root):
    result = tkinter.messagebox.askyesno("Confirm", "Would you like to start a local network?")
    if result is True:
        output_box.config(state=tkinter.NORMAL)
        output_box.delete("1.0", tkinter.END)
        output_box.insert(tkinter.END, "Starting Baby Fleming...\n")
        output_box.config(state=tkinter.DISABLED)

        process = subprocess.Popen(["safe", "node", "run-baby-fleming"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1) 

        def update_progress_bar(thread):
            with tqdm(total=10) as progress_bar:
                while True:
                    try:
                        if thread.poll() is not None:
                            progress_bar.update(10 - progress_bar.n)
                            break

                        output = thread.stdout.readline()
                        if "fleming-nodes/sn-node-11" in output:
                            progress_bar.update(10 - progress_bar.n)
                            output_box.config(state=tkinter.NORMAL)
                            output_box.delete("1.0", tkinter.END)
                            output_box.insert(tkinter.END, "Baby Fleming started successfully!\n")
                            output_box.config(state=tkinter.DISABLED)
                            break

                        progress_bar.update(1)
                        output_box.config(state=tkinter.NORMAL)
                        output_box.delete("1.0", tkinter.END)
                        output_box.insert(tkinter.END, f"Starting Baby Fleming{'.' * (int(progress_bar.n / 10) % 6)}\n") 
                        output_box.config(state=tkinter.DISABLED)
                        root.update()
                        time.sleep(0.08)

                    except:
                        print("Error occurred while updating progress bar")
                        break

        update_thread = threading.Thread(target=update_progress_bar, args=(process,), daemon=True)
        update_thread.start()
        print("Started progress bar thread")

def switch_baby_fleming(output_box):
    try:
        output_box.config(state=tkinter.NORMAL)
        subprocess.check_output(["safe", "networks", "switch", "baby-fleming"], stderr=subprocess.STDOUT) 
        output_box.insert(tkinter.END, "You have switched to the Baby-Fleming network.\n")
    except subprocess.CalledProcessError as e:
        output_box.insert(tkinter.END, e.output.decode())
        output_box.insert(tkinter.END, "Error switching network to Baby-Fleming.\n")
    finally:
        output_box.config(state=tkinter.DISABLED)

def reset_baby_fleming(output_box):
    result = tkinter.messagebox.askyesno("Confirm", "Reset the local network? This cannot be undone.") 
    if result is True:
        try:
            try:
                subprocess.run(["safe", "node", "killall"], check=True)
            except subprocess.CalledProcessError:
                pass

            try:
                shutil.rmtree(os.path.expanduser("~/.safe/node/baby-fleming-nodes"))
            except FileNotFoundError:
                pass

            try:
                dir_path = os.path.expanduser("~/.safe/network_contacts")
                for filename in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if '127.0.0.' in f.read():
                            os.remove(file_path)
            except FileNotFoundError:
                pass

            output_box.config(state="normal")
            output_box.delete("1.0", tkinter.END)
            output_box.insert("1.0", "The local network has been reset.")
            output_box.config(state="disabled")

        except Exception as e:
            output_box.config(state="normal")
            output_box.delete("1.0", tkinter.END)
            output_box.insert("1.0", f"An error occurred while resetting the local network: {e}")
            output_box.config(state="disabled")

def show_networks(output_box):
    try:
        cmd = "safe networks | awk -F'|' 'NR>5 && NF>=5 {print $2,$3,$4}' | sed '/^$/d; /^*$/d'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output_box.config(state="normal")
        output_box.delete("1.0", tkinter.END)
        output_box.insert("1.0", result.stdout)
        output_box.config(state="disabled")

    except Exception as e:
        output_box.config(state="normal")
        output_box.delete("1.0", tkinter.END)
        output_box.insert("1.0", f"An error occurred while running `safe networks`: {e}")
        output_box.config(state="disabled")

def view_button_func(output_box, input_box):
    view_directory = os.path.expanduser("~/Gooey/Downloads/.view")
    if not os.path.exists(view_directory):
        os.makedirs(view_directory)

    command = input_box.get()
    safe_command = "safe cat " + command + " > ~/Gooey/Downloads/.view/download"
    process = subprocess.Popen(safe_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 

    while process.poll() is None:
        time.sleep(0.1)

    if process.returncode != 0:
        output_box.config(state="normal")
        output_box.insert("end", "No safeurl or no active network, select(switch) or add a network.\n") 
        output_box.config(state="disabled")
    else:
        try:
            if platform.system() == "Linux":
                os.system("xdg-open ~/Gooey/Downloads/.view/download")
            #elif platform.system() == "Windows":
                #os.startfile("~/Gooey/Downloads/.view/download")
            elif platform.system() == "Darwin":
                os.system("open ~/Gooey/Downloads/.view/download")
        except Exception as e:
            output_box.config(state="normal")
            output_box.insert("end", "An error occurred: " + str(e) + "\n")
            output_box.config(state="disabled")

def upload_file(box, input_box):
    file_path = input_box.get()
    if file_path:
        file_path = os.path.expanduser(f'{file_path}')
        file_path = os.path.normpath(file_path)
        print(f"Cleaned file path: {file_path}")

        if not os.path.exists(file_path):
            print(f"Error: File path {file_path} does not exist.")
            return

        input_box.delete(0, tkinter.END)
        input_box.insert(0, file_path)
        command = f'safe files put "{file_path}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) 
        output = process.stdout.read() + process.stderr.read()
        output_file = f'{os.path.expanduser("~")}/Gooey/upload.txt'
        with open(output_file, 'a') as f:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            f.write(f'{now} - File: {file_path}\n{output}\n\n')
        box.configure(state="normal")
        box.insert(tkinter.END, output)
        box.configure(state="disabled")

def upload_folder(box, input_box):
    folder_path = input_box.get()
    if folder_path:
        folder_path = os.path.expanduser(f'{folder_path}')
        folder_path = os.path.normpath(folder_path)
        print(f"Cleaned folder path: {folder_path}")

        if not os.path.exists(folder_path):
            print(f"Error: Folder path {folder_path} does not exist.")
            return

        input_box.delete(0, tkinter.END)
        input_box.insert(0, folder_path)
        command = f'safe files put "{folder_path}"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) 
        output = process.stdout.read() + process.stderr.read()
        output_file = f'{os.path.expanduser("~")}/Gooey/upload.txt'
        with open(output_file, 'a') as f:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            f.write(f'{now} - Folder: {folder_path}\n{output}\n\n')
        box.configure(state="normal")
        box.insert(tkinter.END, output)
        box.configure(state="disabled")

def upload_history(output_box):
    file_path = os.path.join(os.path.expanduser("~/Gooey"), "upload.txt")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            contents = file.read()
            output_box.config(state="normal")
            output_box.delete('1.0', 'end')
            output_box.insert('1.0', contents)
            output_box.config(state="disabled")
    else:
        output_box.config(state="normal")
        output_box.delete('1.0', 'end')
        output_box.insert('1.0', "No upload history found.")
        output_box.config(state="disabled")

def clear_history(output_box):
    file_path = os.path.join(os.path.expanduser("~/Gooey"), "upload.txt")
    if os.path.exists(file_path):
        confirmed = tkinter.messagebox.askyesno("Confirm", "Are you sure you want to clear the upload history?") 
        if confirmed:
            os.remove(file_path)
            output_box.config(state="normal")
            output_box.delete("1.0", tkinter.END)
            output_box.insert("1.0", "Upload history cleared.")
            output_box.config(state="disabled")
        else:
            output_box.config(state="normal")
            output_box.delete("1.0", tkinter.END)
            output_box.insert("1.0", "Upload history was not cleared.")
            output_box.config(state="disabled")
    else:
        output_box.config(state="normal")
        output_box.delete("1.0", tkinter.END)
        output_box.insert("1.0", "No upload history found.")
        output_box.config(state="disabled")

def delete_downloads(output_box):
    dir_path = os.path.join(os.path.expanduser("~/Gooey"), "Downloads")
    if os.path.exists(dir_path):
        confirmed = tkinter.messagebox.askyesno("Confirm", "Delete all Downloads?")
        if confirmed:
            shutil.rmtree(dir_path)
            os.makedirs(dir_path)
            output_box.config(state="normal")
            output_box.delete("1.0", tkinter.END)
            output_box.insert("1.0", "Downloads folder cleared.")
            output_box.config(state="disabled")
        else:
            output_box.config(state="normal")
            output_box.delete("1.0", tkinter.END)
            output_box.insert("1.0", "Downloads folder was not cleared.")
            output_box.config(state="disabled")
    else:
        output_box.config(state="normal")
        output_box.delete("1.0", tkinter.END)
        output_box.insert("1.0", "No Downloads folder found.")
        output_box.config(state="disabled")

def container_contents(output_box, input_box):
    container_address = input_box.get()
    if not container_address.startswith("safe://") or "?v=" not in container_address:
        output_box.config(state="normal")
        output_box.insert("end", "Not a container.\n")
        output_box.config(state="disabled")
        return

    command = ["safe", "cat", container_address]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output_box.config(state="normal")
        output_box.insert("end", result.stdout)
        output_box.config(state="disabled")
    except subprocess.CalledProcessError as e:
        output_box.config(state="normal")
        output_box.insert("end", f"Error running `files {container_address}`: {e.output}\n")
        output_box.config(state="disabled")

def save_file(output_box, input_box):
    view_directory = os.path.expanduser("~/Gooey/Downloads/.view")
    if not os.path.exists(view_directory):
        os.makedirs(view_directory)

    media_type_command = f"safe dog {input_box.get()}"
    media_type_process = subprocess.Popen(media_type_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    media_type_output, _ = media_type_process.communicate()

    if media_type_process.returncode != 0:
        output_box.config(state="normal")
        output_box.insert("end", "No safeurl or no active network, select(switch) or add a network.\n")
        output_box.config(state="disabled")
        return
    else:
        lines = media_type_output.decode('utf-8').split("\n")
        media_type_line = next((line for line in lines if line.startswith("Media type:")), None)
        if not media_type_line:
            output_box.config(state="normal")
            output_box.insert("end", "Could not determine media type.\n")
            output_box.config(state="disabled")
            return
        media_type = media_type_line.split(": ")[1].strip()
        extension = media_type.split("/")[-1]
        initial_dir = os.path.expanduser("~/Gooey/Downloads")
        default_filename = ""
        new_filename = filedialog.asksaveasfilename(initialdir=initial_dir, initialfile=default_filename, title="Save As", filetypes=[(media_type, f"*.{extension}")])
        if not new_filename:
            return
        else:
            filename = os.path.basename(new_filename)
            safe_command = f"safe cat {input_box.get()} > {new_filename}"
            process = subprocess.Popen(safe_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            while process.poll() is None:
                time.sleep(0.1)

            if process.returncode != 0:
                output_box.config(state="normal")
                output_box.insert("end", "No safeurl or no active network, select(switch) or add a network.\n")
                output_box.config(state="disabled")
            else:
                output_box.config(state="normal")
                output_box.insert("end", f"File {filename} saved successfully.\n")
                output_box.config(state="disabled")
