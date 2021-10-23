import threading

import yaml

from src.common.config import GeneralConfig


class Config(GeneralConfig):
    def __init__(self):
        super().__init__("src/decision/reinforcement_learning/config/config.yaml")
        with open(self.file_path, "r") as configfile:
            self.data = yaml.load(configfile, Loader=yaml.FullLoader)
        watcher_thread = threading.Thread(target=super().watch_config)
        watcher_thread.setDaemon(True)
        watcher_thread.start()

    def get_logging_level(self):
        return self.data['logging-level']

    def get_basic_reward(self):
        return self.data['basic-reward']

    def is_mode_active(self, mode):
        return self.data['reward-modes'][mode]['active']

    def get_reward_ranges(self, mode):
        if 'ranges' in self.data['reward-modes'][mode]:
            return self.data['reward-modes'][mode]['ranges']
        return []

    def is_ev3(self):
        return self.data['ev3']
