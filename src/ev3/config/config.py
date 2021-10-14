import yaml

from src.common.config import GeneralConfig


class Config(GeneralConfig):
    def __init__(self):
        super().__init__("src/ev3/config/config.yaml")
        with open(self.file_path, "r") as configfile:
            self.data = yaml.load(configfile, Loader=yaml.FullLoader)
        # TODO: call the following method in background thread:
        # super().watch_config(self.on_modified)

    def get_logging_level(self):
        return self.data['logging-level']

    def get_directory_to_observe(self):
        return self.data['smt']['watch-directory']

    def get_solver_installation_location(self):
        return self.data['smt']['installation-location']
