#!/usr/bin/env python3

import requests

API_URL = "http://127.0.0.1:5000/formulae"
FORM_DATA_PARAM_KEY = "formula_file"


def post_smt_problem(smt_file):
    file = open(smt_file, "rb")
    response = requests.post(API_URL, files={FORM_DATA_PARAM_KEY: file})
    file.close()
    return response
