#!/usr/bin/env python3

import subprocess


def call_solver(solver_location, filename):
    process = subprocess.run([solver_location, filename], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    return output
