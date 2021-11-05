import threading

import yaml

from src.common.config import GeneralConfig


class Config(GeneralConfig):
    def __init__(self):
        super().__init__("src/monitoring/config/config.yaml")
        with open(self.file_path, "r") as configfile:
            self.data = yaml.load(configfile, Loader=yaml.FullLoader)
        watcher_thread = threading.Thread(target=super().watch_config)
        watcher_thread.setDaemon(True)
        watcher_thread.start()

    def get_logging_level(self):
        return self.data['logging-level']

    def get_indicator_ranges(self, indicator):
        return self.data['indicators'][indicator]

    def is_simulation_active(self):
        return self.data['simulation']['active']

    def get_simulated_value(self, indicator):
        return self.data['simulation']['values'][indicator]

    def is_ev3(self):
        return self.data['ev3']
