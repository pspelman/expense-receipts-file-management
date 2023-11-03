import inspect
import os
import subprocess
import sys
import shutil
from datetime import datetime

from watchdog.observers import Observer

from file_watcher import FileMonitor


def get_directory_path_of_file(file_path):
    return os.path.abspath(os.path.dirname(file_path))


def open_file_with_system_default(file_path):
    print(f"opening '{os.path.basename(file_path)}'...")
    if sys.platform == "darwin":  # macOS
        subprocess.run(["open", file_path])
    elif sys.platform == "linux2" or sys.platform == "linux":
        subprocess.run(["xdg-open", file_path])
    elif sys.platform == "win32":
        subprocess.run("start", file_path, shell=True)
    else:
        raise ValueError(f"Unable to determine operating system '{sys.platform}'")


def open_in_file_manager(file_path):
    if sys.platform == "darwin":  # macOS
        subprocess.run(["open", "-R", file_path])
    elif sys.platform == "linux2" or sys.platform == "linux":
        # warning that this will open the directory but may not highlight the file
        subprocess.run(["xdg-open", os.path.dirname(file_path)])
    elif sys.platform == "win32":
        subprocess.run(["explorer", "/select", os.path.abspath(file_path)])
    else:
        raise ValueError(f"Unable to determine operating system '{sys.platform}'")


def open_file_and_monitor(file_path):
    if sys.platform != "darwin":
        raise EnvironmentError(
            f"{inspect.currentframe().f_code.co_name} can only be used on macOS"
        )

    # open the file
    subprocess.Popen(["open", file_path])

    # set up an observer
    observer = Observer()
    event_handler = FileMonitor(file_path, observer)
    dir_path = get_directory_path_of_file(file_path)
    observer.schedule(event_handler, path=dir_path, recursive=False)
    observer.start()

    try:
        while observer.is_alive():
            # could add logic here to stop observing after some condition
            # e.g., after a certain time period or if a certain flag is set.
            observer.join(1)
    except KeyboardInterrupt:
        print("Observer was interrupted... stopping observation")
        observer.stop()

    observer.join()


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


def update_file_actions_log(details, log_file="default"):
    print(f"updating the files actions log")


def log_event(details, log_dir=None, log_file="interaction_log.txt"):
    log_file_path = f"{log_dir}/{log_file}" if log_dir else log_file
    with open(log_file_path, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp}|{details}\n")


def move_file_to_done_dir(source_file_path, done_dir="entered", log_file_dir=None):
    file_name = os.path.basename(source_file_path)
    print(f"moving {source_file_path} to {done_dir}")
    file_dir_path = get_directory_path_of_file(source_file_path)
    try:
        os.chdir(file_dir_path)
    except FileNotFoundError:
        print(f"Directory {file_dir_path} does not exist.")
    try:
        print(f"Changed directory to {file_dir_path}")
        current_dir = os.path.dirname(source_file_path)
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        print(f"parent dir: {parent_dir}")
        destination_path = f"{parent_dir}/{done_dir}/{file_name}"
        print(f"FAKE moving file to {destination_path}")
        shutil.move(source_file_path, destination_path)
        log_event(f"MOVED_FILE: {source_file_path} --> {destination_path}", log_file_dir, "moved_files_log.txt")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_todo_items(dir_paths, pending_items_dir_name="todo"):
    todos = set()
    for dir_path in dir_paths:
        if "todo" in get_subdir_names(dir_path):
            # get the file_names in the todo folder
            path_todo_dir = f"{dir_path}/{pending_items_dir_name}"
            dir_todo_files = [
                f"{path_todo_dir}/{file_name}"
                for file_name in os.listdir(path_todo_dir)
                if os.path.isfile(os.path.join(path_todo_dir, file_name))
                # and ".DS_Store" not in file_name
                and not file_name.startswith(".")
            ]
            todos = todos.union(set(dir_todo_files))

    return todos
