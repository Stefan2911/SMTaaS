import threading

import yaml

from src.common.config import GeneralConfig


class Config(GeneralConfig):
    def __init__(self):
        super().__init__("src/ev3/config/config.yaml")
        with open(self.file_path, "r") as configfile:
            self.data = yaml.load(configfile, Loader=yaml.FullLoader)
        watcher_thread = threading.Thread(target=super().watch_config)
        watcher_thread.setDaemon(True)
        watcher_thread.start()

    def get_logging_level(self):
        return self.data['logging-level']

    def get_directory_to_observe(self):
        return self.data['smt']['watch-directory']