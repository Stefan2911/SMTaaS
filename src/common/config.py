import os
import time

import yaml
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class GeneralConfig():

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def on_modified(self, event):
        if event.src_path.endswith(os.path.basename(self.file_path)):
            with open(self.file_path, "r") as changed_configfile:
                self.data = yaml.load(changed_configfile, Loader=yaml.FullLoader)

    def watch_config(self):
        patterns = "*"
        ignore_patterns = ""
        ignore_directories = True
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_modified = self.on_modified
        my_observer = Observer()
        my_observer.schedule(my_event_handler, os.path.dirname(self.file_path) + os.sep, recursive=False)
        my_observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            my_observer.stop()
        my_observer.join()
