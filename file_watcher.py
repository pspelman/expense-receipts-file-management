import time
import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileMonitor(FileSystemEventHandler):
    # the FileMonitor will watch a file and respond when changes to the file occur
    def __init__(self, filename, observer):
        self.filename = filename
        self.observer = observer

    def on_modified(self, event):
        if event.src_path == self.filename:
            print(f"{self.filename} was modified.")
            # todo: any instructions to execute on file modification

    def on_closed(self, event):
        if event.event_type == "closed":
            print(f"{self.filename} was closed")
            self.observer.stop()

    def on_any_event(self, event):
        print(f"An event was detected")
        print(event)
