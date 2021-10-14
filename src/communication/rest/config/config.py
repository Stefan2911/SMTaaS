import yaml

from src.common.config import GeneralConfig


class Config(GeneralConfig):
    def __init__(self):
        super().__init__("src/communication/rest/config/config.yaml")
        with open(self.file_path, "r") as configfile:
            self.data = yaml.load(configfile, Loader=yaml.FullLoader)
        # TODO: call the following method in background thread:
        # super().watch_config(self.on_modified)

    def get_logging_level(self):
        return self.data['logging-level']

    def get_api_url(self):
        return self.data['api-url']

    def get_local_api_url(self):
        return self.data['local-api-url']
