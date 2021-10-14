import time

import yaml
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class GeneralConfig():

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def on_modified(self, event):
        print(event.src_path)
        # TODO: comparison
        # if event.src_path == self.file_path:
        if event.src_path == ".\config.yaml":
            with open(self.file_path, "r") as changed_configfile:
                self.data = yaml.load(changed_configfile, Loader=yaml.FullLoader)

    def watch_config(self):
        patterns = "*"
        ignore_patterns = ""
        ignore_directories = True
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_modified = self.on_modified
        path = "."
        my_observer = Observer()
        my_observer.schedule(my_event_handler, path, recursive=False)
        my_observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            my_observer.stop()
        my_observer.join()
