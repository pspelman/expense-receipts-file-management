# This is a sample Python script.
import json

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import os
import time

from file_methods import open_file_with_system_default


def move_file_to_entered(file_path):
    print(f"moving {file_path} to the 'entered' directory")


def get_subdir_names(target_dir):
    return [
        sub_dir
        for sub_dir in os.listdir(target_dir)
        if os.path.isdir(os.path.join(target_dir, sub_dir))
    ]


def get_subdir_paths(target_dir):
    return [
        f"{target_dir}/{sub_dir}"
        for sub_dir in os.listdir(target_dir)
        if os.path.isdir(os.path.join(target_dir, sub_dir))
    ]


# Press the green button in the gutter to run the script.
def get_todo_items(dir_paths):
    todos = set()
    for dir_path in dir_paths:
        if "todo" in get_subdir_names(dir_path):
            # get the filenames in the todo folder
            path_todo_dir = f"{dir_path}/todo"
            dir_todo_files = [
                f"{path_todo_dir}/{filename}"
                for filename in os.listdir(path_todo_dir)
                if os.path.isfile(os.path.join(path_todo_dir, filename))
                and ".DS_Store" not in filename
            ]
            print(f"adding todo items from {dir_path} ...")
            print(json.dumps(dir_todo_files, indent=4, sort_keys=True))
            todos = todos.union(set(dir_todo_files))

    return todos


def process_todo_items(todo_list):
    total_items = len(todo_list)
    print(f"there are {total_items} items to process")
    input("press return to begin")
    for item in todo_list:
        print(f"processing '{os.path.basename(item)}'")
        input("press the return key to continue")
        open_file_with_system_default(item)
        # TODO: ask if the user wants to move the file to complete or skip to the next file



if __name__ == "__main__":
    # TODO: set the path to scan
    base_path = "/Users/phil/Library/CloudStorage/GoogleDrive-phil@sisusifu.com/Shared drives/SisuSifu"
    expense_receipts_path = f"{base_path}/SS - Receipts - 2023"
    print(f"scanning path: {expense_receipts_path}")
    # all sub-directories
    dirs = get_subdir_names(expense_receipts_path)
    print(json.dumps(dirs, indent=4, sort_keys=True))

    dir_paths = get_subdir_paths(expense_receipts_path)
    print(json.dumps(dir_paths, indent=4, sort_keys=True))

    # TODO: check each path for a "todo" directory
    #  if it exists, get the list of files in it
    items_todo = sorted(list(get_todo_items(dir_paths)))
    print(json.dumps(items_todo, indent=4, sort_keys=True))

    if len(items_todo):
        process_todo_items(items_todo)

    # TODO: start a loop scanning the path for every folder with a todo
    # TODO: grab the name of the parent folder (e.g., "hardware") that comes before the todo directory
    # TODO: get a list of files within every "todo" directory
    # TODO: start with the top file and wait for user input
    #   user has instructions for skip, complete, move to 'entered' directory
    #

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
