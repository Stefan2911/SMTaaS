#!/usr/bin/env python3

import requests

from src.communication.rest.config.config import Config

FORM_DATA_PARAM_KEY = "formula_file"


class Client():
    def __init__(self):
        self.config = Config()

    def post_smt_problem_offload(self, smt_file):
        return self.__post_smt_problem(smt_file, self.config.get_api_url())

    def post_smt_problem_local(self, smt_file):
        return self.__post_smt_problem(smt_file, self.config.get_local_api_url())

    def __post_smt_problem(self, smt_file, url):
        file = open(smt_file, "rb")
        response = requests.post(url, files={FORM_DATA_PARAM_KEY: file})
        file.close()
        return response
