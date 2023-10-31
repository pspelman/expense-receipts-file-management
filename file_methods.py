import os
import sys
import subprocess


def open_file_with_system_default(filepath):
    print(f"opening '{os.path.basename(filepath)}'...")
    if sys.platform == "darwin":  # macOS
        subprocess.run(["open", filepath])
    elif sys.platform == "linux2" or sys.platform == "linux":
        subprocess.run(["xdg-open", filepath])
    elif sys.platform == "win32":
        subprocess.run("start", filepath, shell=True)
    else:
        raise ValueError(f"Unable to determine operating system '{sys.platform}'")


def open_in_file_manager(filepath):
    if sys.platform == "darwin":  # macOS
        subprocess.run(["open", "-R", filepath])
    elif sys.platform == "linux2" or sys.platform == "linux":
        # warning that this will open the directory but may not highlight the file
        subprocess.run(["xdg-open", os.path.dirname(filepath)])
    elif sys.platform == "win32":
        subprocess.run(["explorer", "/select", os.path.abspath(filepath)])
    else:
        raise ValueError(f"Unable to determine operating system '{sys.platform}'")
