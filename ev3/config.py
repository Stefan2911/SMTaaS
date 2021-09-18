import yaml

with open("config.yaml", "r") as configfile:
    data = yaml.load(configfile, Loader=yaml.FullLoader)


def get_logging_level():
    return data['logging-level']


def get_api_url():
    return data['api-url']


def get_indicator_configuration():
    return data['decision-making']['indicators']


def get_offload_threshold():
    return data['decision-making']['offload-threshold']


def get_update_interval():
    return data['decision-making']['update-interval']


def get_directory_to_observe():
    return data['smt']['watch-directory']


def get_solver_installation_location():
    return data['smt']['installation-location']
