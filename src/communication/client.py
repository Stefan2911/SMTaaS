#!/usr/bin/env python3

import requests

FORM_DATA_PARAM_KEY = "formula_file"


def post_smt_problem(smt_file, url):
    with open(smt_file, 'rb') as file:
        response = requests.post(url, files={FORM_DATA_PARAM_KEY: file}, timeout=60)  # 1 minute
        return response.text
