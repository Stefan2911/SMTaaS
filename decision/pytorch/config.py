import time

import yaml
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

with open("config.yaml", "r") as configfile:
    data = yaml.load(configfile, Loader=yaml.FullLoader)


def get_hyper_parameters():
    return data['hyper-parameters']


def is_mode_active(mode):
    return data['reward-modes'][mode]['active']


def get_reward_ranges(mode):
    return data['reward-modes'][mode]['ranges']


def on_modified(event):
    if event.src_path == ".\config.yaml":
        with open("config.yaml", "r") as changed_configfile:
            global data
            data = yaml.load(changed_configfile, Loader=yaml.FullLoader)


def watch_config():
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_modified = on_modified
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


if __name__ == "__main__":
    watch_config()
