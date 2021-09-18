#!/usr/bin/env python3

import requests

FORM_DATA_PARAM_KEY = "formula_file"


def post_smt_problem(smt_file, api_url):
    file = open(smt_file, "rb")
    response = requests.post(api_url, files={FORM_DATA_PARAM_KEY: file})
    file.close()
    return response
