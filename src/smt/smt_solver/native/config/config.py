import threading

import yaml

from src.common.config import GeneralConfig


class Config(GeneralConfig):
    def __init__(self):
        super().__init__("src/smt/smt_solver/native/config/config.yaml")
        with open(self.file_path, "r") as configfile:
            self.data = yaml.load(configfile, Loader=yaml.FullLoader)
        watcher_thread = threading.Thread(target=super().watch_config)
        watcher_thread.setDaemon(True)
        watcher_thread.start()

    def get_solver_location(self):
        return self.data['solver-location']

    def is_final_node(self):
        return self.data['final-node']
