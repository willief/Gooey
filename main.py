"""
GUI application for the SAFE network. 

"""
import os

import sys

import json

import subprocess

import tkinter as tk

from tkinter import messagebox

from tkinter import ttk

import random

from PIL import Image

from button_functions import (install_safe, install_node, safe_version, safe_rm, jpl_primer, about_info,
                              add_maidsafe, switch_maidsafe, add_comnet, switch_comnet, kill_node, run_baby_fleming, reset_baby_fleming, switch_baby_fleming, show_networks,
                              view_button_func, upload_file, upload_folder, upload_history, clear_history, delete_downloads, container_contents, save_file)

script_dir = os.path.dirname(os.path.abspath(__file__))

buttons_file = os.path.join(script_dir, 'buttons.json')

current_file_path = os.path.abspath(__file__)

current_directory = os.path.dirname(current_file_path)

buttons_file_path = os.path.join(current_directory, 'path', 'to', 'buttons.json')

#messagebox.showinfo("Welcome!", "Welcome to Gooey!\nIf you dbl clicked on the AppImage this will not work.\nStart the App from the command line.\nRight clicking on the file tree will add the path for upload.")

# Window
root = tk.Tk()
root.title("Gooey")
root.geometry("1400x870")
root.configure(background="#3d3d3d")
root.wm_minsize(1080, 650)
root.maxsize(1550, 930)

# Style
style = ttk.Style(root)
style.theme_use("default")
style.configure(".", background="#3d3d3d", foreground="white")
style.configure("Tur.TButton", background="#347582", width=18, height=1.8)
style.configure("TNotebook.Tab", background="#246673", foreground="white")
style.map("TNotebook.Tab", background=[("selected", "#a83838")], foreground=[("selected", "white")])
style.map("TButton", background=[("active", "#a83838")])
style.configure("Treeview", background="#3d3d3d", fieldbackground="#3d3d3d", foreground="white")
style.map("Treeview", background=[("selected", "#a34f49")], foreground=[("selected", "white")])
style.map("TEntry", foreground=[("active", "white"), ("!disabled", "white")])
style.configure("TEntry", fieldbackground="#4d3d3d")

font = ("Monospace", 10)
for child in root.winfo_children():
    if isinstance(child, tk.Widget):
        child.configure(font=font)
input_frame = ttk.Frame(root, padding=10)
input_frame.pack(fill=tk.X, side=tk.TOP)

# Def clear input
def clear_input_box():
    input_box.delete(0, 'end')

# Input box
input_box = ttk.Entry(root, style="TEntry")
input_box.pack(fill=tk.X, expand=False, padx=10, pady=10)
input_box.configure(font=("Arial"))
input_box.insert(0, "safe://")

# Clear button input_box
clear_button = ttk.Button(
    input_box, text="x", command=clear_input_box, style="Clear.TButton")
clear_button.pack(side="right", padx=0)

# Clear button style
style.configure("Clear.TButton", background="#3d3d3d",
                foreground="#FFFFFF", width=1, padding=3, borderwidth=0)

# Paste input-box
def on_return(event):
    if input_box.get() == "safe://":
        input_box.delete(0, tk.END)

def on_paste(event):
    if input_box.get() == "safe://":
        input_box.delete(0, tk.END)

input_box.bind("<<Paste>>", on_paste)

menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Paste")

def show_menu(event):
    menu.post(event.x_root, event.y_root)

input_box.bind("<Button-3>", show_menu)

def paste():
    input_box.event_generate('<<Paste>>')

menu.entryconfig("Paste", command=paste)

def hide_menu(event):
    menu.unpost()

root.bind("<Button-1>", hide_menu)

#Check for and create Gooey Directory
safe_uploads_path = os.path.join(os.path.expanduser("~"), "Gooey")
if not os.path.exists(safe_uploads_path):
    os.makedirs(safe_uploads_path)

downloads_path = os.path.join(safe_uploads_path, "Downloads")
if not os.path.exists(downloads_path):
    os.makedirs(downloads_path)

temp_path = os.path.join(downloads_path, ".view")
if not os.path.exists(temp_path):
    os.makedirs(temp_path)

upload_log_path = os.path.join(safe_uploads_path, "upload.txt")
if not os.path.exists(upload_log_path):
    with open(upload_log_path, "w", encoding="utf-8") as f:
        pass

def toggle_tree_frame(width=10):
    if tree_frame.winfo_width() > width:
        tree_frame.width = tree_frame.winfo_width()
        tree_frame.pack_forget()
        tree_frame.config(width=width)
    else:
        tree_frame.config(width=tree_frame.width)
        tree_frame.pack(side=tk.LEFT, fill=tk.Y)

# Create the tree_frame.
tree_frame = ttk.Frame(root, width=600, height=400)
tree_frame.pack_forget()  # Hide the frame initially
tree_frame['padding'] = (10, 10)

# Define a function to toggle the visibility of the tree_frame
def toggle_tree_frame():
    if tree_frame.winfo_viewable():
        tree_frame.pack_forget()
    else:
        tree_frame.pack(fill=tk.BOTH, expand=True)

# Add a keyboard shortcut to toggle the visibility of the tree_frame
root.bind("<Control-f>", lambda event: toggle_tree_frame())

# Add a button to toggle the visibility of the tree_frame
left_button = ttk.Button(root, text="Filesystem (Ctrl+F)", command=toggle_tree_frame)
left_button.pack(side=tk.BOTTOM)


# File Tree
class Node:
    """
    A simple class to represent a file or directory in the filesystem.
    """
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.is_directory = os.path.isdir(path)
        self.children = []
        self.size = os.path.getsize(path) if not self.is_directory else 0

    def add_child(self, child):
        self.children.append(child)
        self.size += child.size

    def __str__(self):
        return self.name

def display_file(file_path):
    if os.path.isfile(file_path):
        # Use subprocess to open the file with the default application
        subprocess.run(['xdg-open', file_path], check=True)

def populate_treeview(treeview, node, parent_id=''):
    item_id = treeview.insert(parent_id, "end", text=node.name, open=False)

    # Add size to the treeview.
    size = node.size
    if size < 1024:
        size_str = f"{size} B"
    elif size < 1024 ** 2:
        size_str = f"{size / 1024:.2f} KB"
    elif size < 1024 ** 3:
        size_str = f"{size / 1024 ** 2:.2f} MB"
    else:
        size_str = f"{size / 1024 ** 3:.2f} GB"
    treeview.set(item_id, "#1", size_str)

    # Add child nodes.
    for child in node.children:
        if child.is_directory:
            populate_treeview(treeview, child, parent_id=item_id)
        else:
            child_item_id = treeview.insert(item_id, "end", text=child.name)
            size = child.size
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 ** 2:
                size_str = f"{size / 1024:.2f} KB"
            elif size < 1024 ** 3:
                size_str = f"{size / 1024 ** 2:.2f} MB"
            else:
                size_str = f"{size / 1024 ** 3:.2f} GB"
            treeview.set(child_item_id, "#1", size_str)

            # Open files
            ext = os.path.splitext(child.name)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff', '.webp', '.ico']:
                treeview.item(child_item_id, tags=("image", child.path))
                treeview.tag_bind("image", "<Double-1>", lambda event: Image.open(treeview.item(treeview.selection())['tags'][1]).show())

            elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.gif']:
                treeview.item(child_item_id, tags=("video", child.path))
                treeview.tag_bind("video", "<Double-1>", lambda event: os.system(f"xdg-open '{treeview.item(treeview.selection())['tags'][1]}'"))
            elif ext in ['.txt', '.md']:
                treeview.item(child_item_id, tags=("text", child.path))
                treeview.tag_bind("text", "<Double-1>", lambda event: subprocess.run(['xdg-open', treeview.item(treeview.selection())['tags'][1]], shell=True, check=True))

            else:
                treeview.item(child_item_id, tags=("file", child.path))
                treeview.tag_bind("file", "<Double-1>", lambda event: display_file(treeview.item(treeview.selection())['tags'][1]))

        # Bind right-click event to treeview
        treeview.bind("<Button-3>", lambda event: on_tree_right_click(event, treeview))

def create_filesystem_treeview(parent):
    """
    Create a filesystem treeview and return its root node.
    """
    root_node = ttk.Treeview(parent, columns=("Size"))
    root_node.heading("#0", text="Filesystem", anchor="w")
    root_node.heading("#1", text="Size", anchor="e")
    root_node.column("#0", width=580)
    root_node.column("#1", width=80, anchor="e")
    
    # Populate the treeview with the contents of the root directory.
    root_dir = '/'
    current_node = Node(root_dir)
    populate_directory(current_node, max_depth=2)
    populate_treeview(root_node, current_node)

    return root_node

def on_tree_right_click(event, treeview):
    item = treeview.identify_row(event.y)
    path = treeview.item(item, "text")
    parent = treeview.parent(item)
    while parent != "":
        path = treeview.item(parent, "text") + "/" + path
        parent = treeview.parent(parent)
    input_box.delete(0, tk.END)
    input_box.insert(0, path)

def populate_directory(directory_node, depth=0, max_depth=2):
    """
    Recursively populate a directory node with its contents, up to a maximum depth.
    """
    if depth >= max_depth:
        return

    try:
        entries = sorted(os.scandir(directory_node.path), key=lambda entry: entry.name.lower())
        for entry in entries:
            child_node = Node(entry.path)
            directory_node.add_child(child_node)
            if child_node.is_directory:
                if depth == 0 and child_node.name == 'home':
                    # Fully populate the home directory to a depth of 5
                    populate_directory(child_node, depth=depth+1, max_depth=6)
                else:
                    populate_directory(child_node, depth=depth+1, max_depth=max_depth)
    except (PermissionError, OSError):
        pass

filesystem_treeview = create_filesystem_treeview(tree_frame)
filesystem_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Frames, boxes & scroll
output_frame = ttk.Frame(root, padding=10)
output_frame.pack(fill=tk.BOTH, expand=True)

output_box = tk.Text(output_frame, height=5, width=40,
                     state=tk.DISABLED, wrap="word")
output_box.pack(fill=tk.BOTH, expand=True)
output_box.configure(background="#3d3d3d", foreground="white")

scrollbar = ttk.Scrollbar(output_frame, command=output_box.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_box['yscrollcommand'] = scrollbar.set

scrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NE)

button_frame = ttk.Frame(root, padding=10)
button_frame.pack(fill=tk.X, side=tk.BOTTOM)

notebook = ttk.Notebook(button_frame)
notebook.pack(fill=tk.BOTH, expand=True)

theme_frame = ttk.Frame(root, padding=7)
theme_frame.pack(side=tk.RIGHT, fill=tk.Y)

# create a context menu copy
def copy_selection(widget):
    selected_text = widget.selection_get()
    if selected_text:
        root.clipboard_clear()
        root.clipboard_append(selected_text)
    popup_menu.unpost()

def clear_popup(event):
    popup_menu.unpost()

# create a context menu for the output_box
popup_menu = tk.Menu(root, tearoff=0)
popup_menu.add_command(label="Copy", command=lambda: copy_selection(output_box))

# bind the context menu and clear_popup to the output_box
output_box.bind("<Button-3>", lambda event: popup_menu.post(event.x_root, event.y_root))
output_box.bind("<Button-1>", clear_popup)

# Theme StringVar
selected_theme = tk.StringVar(value="dark")

# Create a frame for the radio buttons at the bottom
bottom_frame = ttk.Frame(root, padding=10)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create a new frame at the bottom of the root window
bottom_frame = ttk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create the radio buttons for theme selection
light_button = ttk.Radiobutton(
    bottom_frame, text="Light", variable=selected_theme, value="light", style="TRadiobutton")
dark_button = ttk.Radiobutton(
    bottom_frame, text="Dark", variable=selected_theme, value="dark", style="TRadiobutton")
rand_button = ttk.Radiobutton(
    bottom_frame, text="Rand", variable=selected_theme, value="rand", style="TRadiobutton")

# Pack the radio buttons inside the bottom frame
rand_button.pack(side=tk.RIGHT, padx=10, pady=1)
light_button.pack(side=tk.RIGHT, padx=10, pady=1)
dark_button.pack(side=tk.RIGHT, padx=10, pady=1)


# Random color
def random_color():
    return '#' + ''.join(random.choice('0123456789ABCDEF') for i in range(6))

# Update the theme
def update_theme():
    if selected_theme.get() == "light":
        root.configure(background="#e1e3e6")
        style.configure(".", background="#e1e3e6")
        style.configure("Treeview", background="white", fieldbackground="white", foreground="black")
        output_box.configure(background="#fafcfc", foreground="black")
        input_box.configure(background="#3d3d3d", foreground="black")
        style.map("Treeview", background=[("selected", "#a34f49")], foreground=[("selected", "white")])
        style.map("TEntry", foreground=[("active", "black"), ("!disabled", "black")])
        style.configure("TEntry", fieldbackground="white")
    elif selected_theme.get() == "dark":
        root.configure(background="#3d3d3d")
        style.configure(".", background="#3d3d3d")
        style.configure("Treeview", background="#3d3d3d", fieldbackground="#3d3d3d", foreground="white")
        output_box.configure(background="#3d3d3d", foreground="white")
        input_box.configure(background="#3d3d3d", foreground="white")
        style.map("Treeview", background=[("selected", "#a34f49")], foreground=[("selected", "white")])
        style.map("TEntry", foreground=[("active", "white"), ("!disabled", "white")])
        style.configure("TEntry", fieldbackground="#4d3d3d")
    else:
        color = random_color()
        root.configure(background=color)
        style.configure(".", background=color)

selected_theme.trace_add("write", lambda *_: update_theme())

# Clear outpt_box
def clear_output_box(box):
    """
    Clear the contents of the given output box.
    """
    box.config(state=tk.NORMAL)
    box.delete("1.0", tk.END)
    box.config(state=tk.DISABLED)

def load_button_names():
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(bundle_dir, 'buttons.json')
    with open(file_path, encoding="utf-8") as json_file:
        button_names = json.load(json_file)
    return button_names

# Buttons
with open(buttons_file, encoding="utf-8") as f:
    button_names = json.load(f)

def create_buttons(buttons_frame, buttons_names, box):
    """
    Creates buttons on the given frame with the given names,\
    """
    for i, button_name in enumerate(buttons_names):
        button = ttk.Button(buttons_frame, text=button_name,
                            style="Tur.TButton", padding=15)
        row, col = divmod(i, 4)
        button.grid(row=row, column=col, padx=5, pady=5)
        if button_name == "Install SAFE":
            button.configure(command=lambda: (
                clear_output_box(box), install_safe(box)))
        elif button_name == "Install Node":
            button.configure(command=lambda: (
                clear_output_box(box), install_node(box, root)))
        #elif button_name == "Start a Node":
            #button.configure(command=lambda: (
                #clear_output_box(box), node_join(box)))
        elif button_name == "Check Version":
            button.configure(command=lambda: (
                clear_output_box(box), safe_version(box)))
        elif button_name == "Uninstall":
            button.configure(command=lambda: (
                clear_output_box(box), safe_rm(box)))
        elif button_name == "Primer":
            button.configure(command=lambda: (
                clear_output_box(box), jpl_primer()))
        elif button_name == "About":
            button.configure(command=lambda: (
                clear_output_box(box), about_info(box)))
        elif button_name == "Add Maidsafe":
            button.configure(command=lambda: (
                clear_output_box(box), add_maidsafe(box)))
        elif button_name == "Switch Maidsafe":
            button.configure(command=lambda: (
                clear_output_box(box), switch_maidsafe(box)))
        elif button_name == "Add Comnet":
            button.configure(command=lambda: (
                clear_output_box(box), add_comnet(box)))
        elif button_name == "Switch Comnet":
            button.configure(command=lambda: (
                clear_output_box(box), switch_comnet(box)))
        elif button_name == "Kill Node":
            button.configure(command=lambda: (
                clear_output_box(box), kill_node(box)))
        elif button_name == "Run Baby-Fleming":
            button.configure(command=lambda: (
                clear_output_box(box), run_baby_fleming(box, root)))
        elif button_name == "Switch Baby-Fleming":
            button.configure(command=lambda: (
                clear_output_box(box), switch_baby_fleming(box)))
        elif button_name == "Reset Baby-Fleming":
            button.configure(command=lambda: (
                clear_output_box(box), reset_baby_fleming(box)))
        elif button_name == "Show Networks":
            button.configure(command=lambda: (
                clear_output_box(box), show_networks(box)))
        elif button_name == "View":
            button.configure(command=lambda: (
                view_button_func(box, input_box)))
            input_box.bind(
                "<Return>", lambda event: view_button_func(box, input_box))
        elif button_name == "Upload File":
            button.configure(command=lambda: (
                clear_output_box(box), upload_file(box, input_box)))
        elif button_name == "Upload Folder":
            button.configure(command=lambda: (
                clear_output_box(box), upload_folder(box, input_box)))
        elif button_name == "Upload History":
            button.configure(command=lambda: (
                clear_output_box(box), upload_history(box)))
        elif button_name == "Clear History":
            button.configure(command=lambda: (
                clear_output_box(box), clear_history(box)))
        elif button_name == "Delete Downloads":
            button.configure(command=lambda: (
                clear_output_box(box), delete_downloads(box)))
        elif button_name == "Container Contents":
            button.configure(command=lambda: (
                clear_output_box(box), container_contents(box, input_box)))
        elif button_name == "Save":
            button.configure(command=lambda: (
                save_file(box, input_box)))
            input_box.bind(
                "<Return>", lambda event: save_file(box, input_box))

# Tabs
for tab, tab_button_names in button_names.items():
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=tab)
    create_buttons(frame, tab_button_names, output_box)

root.mainloop()
