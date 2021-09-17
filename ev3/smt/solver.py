#!/usr/bin/env python3

import subprocess

SOLVER_LOCATION = "/home/robot/cvc4"


def call_solver(filename):
    process = subprocess.run([SOLVER_LOCATION, filename], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    return output
