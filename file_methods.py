import inspect
import json
import os
import sys
import subprocess

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


def move_file_to_done_dir(file_path):
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


def get_todo_items(dir_paths, pending_items_dir_name="todo"):
    todos = set()
    for dir_path in dir_paths:
        if "todo" in get_subdir_names(dir_path):
            # get the filenames in the todo folder
            path_todo_dir = f"{dir_path}/{pending_items_dir_name}"
            dir_todo_files = [
                f"{path_todo_dir}/{filename}"
                for filename in os.listdir(path_todo_dir)
                if os.path.isfile(os.path.join(path_todo_dir, filename))
                # and ".DS_Store" not in filename
                and not filename.startswith(".")
            ]
            print(f"adding todo items from {dir_path} ...")
            print(json.dumps(dir_todo_files, indent=4, sort_keys=True))
            todos = todos.union(set(dir_todo_files))

    return todos
