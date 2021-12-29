#!/usr/bin/env python3
import logging
import time

import requests

from src.config.config import Config

FORM_DATA_PARAM_KEY = "formula_file"

config = Config()

logging.basicConfig()
logger = logging.getLogger('client')
logger.setLevel(level=config.get_logging_level())


def post_smt_problem(smt_file, url):
    with open(smt_file, 'rb') as file:
        response = requests.post(url, files={FORM_DATA_PARAM_KEY: file}, timeout=60)  # 1 minute
        time.sleep(config.get_simulated_additional_latency())
        return response.text
