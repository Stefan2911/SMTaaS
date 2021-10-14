import yaml

from src.common.config import GeneralConfig


class Config(GeneralConfig):
    def __init__(self):
        super().__init__("src/decision/reinforcement_learning/pytorch/config/config.yaml")
        with open(self.file_path, "r") as configfile:
            self.data = yaml.load(configfile, Loader=yaml.FullLoader)
        # TODO: call the following method in background thread:
        # super().watch_config(self.on_modified)

    def get_logging_level(self):
        return self.data['logging-level']

    def get_basic_reward(self):
        return self.data['basic-reward']

    def get_hyper_parameters(self):
        return self.data['hyper-parameters']

    def is_mode_active(self, mode):
        return self.data['reward-modes'][mode]['active']

    def get_reward_ranges(self, mode):
        return self.data['reward-modes'][mode]['ranges']
