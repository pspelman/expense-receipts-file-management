import os
import tkinter as tk
from tkinter import filedialog, messagebox

from file_methods import open_file_with_system_default


# create the directory opener UI
class DirectoryOpenerApp:
    def __init__(self, _root, _base_path=""):
        self.files_to_process = set()
        self.num_files_to_process = 0
        self.set_dir_btn = None
        self.items_frame = None
        self.items_label = "Select a directory to begin"
        self.root = _root
        self.root.title("Directory Opener")

        # create the control frame
        # create a frame for control buttons
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(padx=10, pady=10, fill="x")

        # set up control buttons
        self.init_control_buttons()

        # Frame for dir contents buttons
        self.update_items_frame()

        self.working_directory = _base_path

    def init_control_buttons(self):
        self.set_dir_btn = tk.Button(
            self.control_frame,
            text="Select Working Directory",
            command=self.set_working_directory,
        )
        self.set_dir_btn.pack(side="left", fill="x", expand=True)
        self.clear_items_btn = tk.Button(
            self.control_frame, text="Clear items", command=self.clear_items_frame
        )
        self.clear_items_btn.pack(side="right", fill="x", expand=True)

    def update_items_frame(self):
        if self.items_frame:
            print(f"clearing the items frame first")
            self.items_frame.destroy()

        # create a frame for the file items buttons
        self.items_frame = tk.Frame(self.root, bg="gray", bd=2, relief="sunken")
        self.items_frame.pack(padx=5, pady=5, fill="x", expand=True)
        self.update_items_frame_label()

    def update_items_frame_label(self, num_items=None):
        # add widgets to the frame
        if num_items == 0:
            self.items_label = tk.Label(self.items_frame, text=f"{num_items} items to process")
        else:
            self.items_label = tk.Label(self.items_frame, text=f"{self.num_files_to_process} items to process")
        self.items_label.pack(pady=5)

    def set_working_directory(self, target_dir=None):
        self.num_files_to_process = 0
        target_dir = target_dir if target_dir else filedialog.askdirectory()
        if target_dir:
            self.working_directory = target_dir
            self.list_directory_contents()

    def list_directory_contents(self):
        self.clear_items_frame()
        try:
            files = os.listdir(self.working_directory)
        except Exception as e:
            messagebox.showerror("Error", f"Could not list directory contents: {e}")
            return

        # create buttons for each item
        self.num_files_to_process = 0
        self.files_to_process = set()
        for file_name in files:
            if file_name.startswith("."):  # do not show hidden files
                continue
            self.num_files_to_process += 1
            # could add logic for differentiating between files and folders
            file_path = f"{self.working_directory}/{file_name}"
            btn = tk.Button(
                self.items_frame,
                text=file_name,
                command=lambda f=file_path: self.open_file(f),
            )
            btn.pack(fill="x")
            # btn.pack()

        self.update_items_frame_label()
        # Update the buttons_frame to re-layout its children
        # self.items_frame.update_idletasks()

    def clear_items_frame(self):
        print(f"called clear_items_frame()")
        # clear existing buttons
        for widget in self.items_frame.winfo_children():
            print(f"destroying {widget}")
            widget.destroy()
        self.update_items_frame_label()
        # self.update_items_frame()
        # self.root.update_idletasks()

    def open_file(self, file_path):
        print(f"trying to open file: {file_path}")
        try:
            if os.path.isdir(file_path):
                # this means a directory was selected - could change to the directory and render the contents, or give a message saying it's a directory
                self.clear_items_frame()
                messagebox.showinfo("info", f"{file_path} is a directory")
                self.set_working_directory(file_path)
                self.list_directory_contents()
            else:
                open_file_with_system_default(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")


# create a frame within the main window
# inner_frame = tk.Frame(root, bg="gray", bd=2, relief="sunken")
# inner_frame.pack(padx=10, pady=10, fill="both", expand=True)
# # add widgets to the frame
# label = tk.Label(inner_frame, text="This is a label inside the frame")
# label.pack(pady=5)
# button = tk.Button(inner_frame, text="Click Me")
# button.pack(pady=5)
#


# Create the root window
root = tk.Tk()
root.geometry("1250x810+100+0")
root.title("Main Window")
base_path = "/File/Location/Goes/Here"
app = DirectoryOpenerApp(root, base_path)

# run the app
root.mainloop()
