#!/usr/bin/env python3
import time

import requests

from src.config.config import Config
from src.simulation.simulation import Simulation

FORM_DATA_PARAM_KEY = "formula_file"

config = Config()
is_evaluation = not config.is_training_active()
simulation = Simulation.get_instance()


def post_smt_problem(smt_file, url):
    with open(smt_file, 'rb') as file:
        response = requests.post(url, files={FORM_DATA_PARAM_KEY: file}, timeout=60)  # 1 minute
        if is_evaluation:
            time.sleep(simulation.get_additional_waiting_time(url).total_seconds())
        return response.text
