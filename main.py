import json
import os
import tkinter as tk

from file_manager_ui import DirectoryOpenerApp
from file_methods import (
    open_file_with_system_default,
    get_subdir_names,
    get_subdir_paths,
    get_todo_items,
)


def process_todo_items(todo_list):
    total_items = len(todo_list)
    print(f"there are {total_items} items to process")
    input("press return to begin")
    for item in todo_list:
        next_file = os.path.basename(item)
        input(f"\n\nNEXT: '{next_file}'\n(press return to open)")
        # open_file_and_monitor(file_path=item)
        open_file_with_system_default(file_path=item)
        options = [("Enter")]
        # TODO: ask if the user wants to move the file to complete or skip to the next file


if __name__ == "__main__":
    base_path = "/Users/phil/Library/CloudStorage/GoogleDrive-phil@sisusifu.com/Shared drives/SisuSifu"
    # set the path to scan
    expense_receipts_path = f"{base_path}/SS - Receipts - 2023"

    # if using the UI, create it and use it to get the todo items
    receipt_management_ui = tk.Tk()
    receipt_management_ui.geometry("1250x810+100+0")
    receipt_management_ui.title("Main Window")
    app = DirectoryOpenerApp(receipt_management_ui, base_path)
    receipt_management_ui.mainloop()

    # all subdirectories - paths and names
    # dir_paths = get_subdir_paths(expense_receipts_path)
    # dirs = get_subdir_names(expense_receipts_path)
    #
    # # check each path for a to-do directory
    # #  if it exists, get the list of files in it
    # items_todo = sorted(list(get_todo_items(dir_paths)))
    # print(json.dumps(items_todo, indent=4, sort_keys=True))
    #
    # # the "script-based" version of this project would probably use a loop like this to go through each file
    # if len(items_todo):
    #     process_todo_items(items_todo)

    # TODO: start a loop scanning the path for every folder with a todo
    # TODO: grab the name of the parent folder (e.g., "hardware") that comes before the todo directory
    # TODO: get a list of files within every "todo" directory
    # TODO: start with the top file and wait for user input
    #   user has instructions for skip, complete, move to 'entered' directory
    #

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
