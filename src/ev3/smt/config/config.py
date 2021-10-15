import yaml

from src.common.config import GeneralConfig


class Config(GeneralConfig):
    def __init__(self):
        super().__init__("src/ev3/smt/config/config.yaml")
        with open(self.file_path, "r") as configfile:
            self.data = yaml.load(configfile, Loader=yaml.FullLoader)
        # TODO: call the following method in background thread:
        # super().watch_config(self.on_modified)

    def get_solver_location(self):
        return self.data['solver-location']
