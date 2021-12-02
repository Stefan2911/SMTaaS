import threading

import yaml

from src.common.config import GeneralConfig


class Config(GeneralConfig):
    def __init__(self):
        super().__init__("src/decision/reinforcement_learning/q_learning/config/config.yaml")
        with open(self.file_path, "r") as configfile:
            self.data = yaml.load(configfile, Loader=yaml.FullLoader)
        watcher_thread = threading.Thread(target=super().watch_config)
        watcher_thread.setDaemon(True)
        watcher_thread.start()

    def get_logging_level(self):
        return self.data['logging-level']

    def get_hyper_parameters(self):
        return self.data['hyper-parameters']

    def get_training_smt_problem(self):
        return self.data['training-smt-problem']

    def get_q_table_location(self):
        return self.data['q-table-location']
