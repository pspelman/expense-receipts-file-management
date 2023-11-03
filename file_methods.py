import inspect
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
