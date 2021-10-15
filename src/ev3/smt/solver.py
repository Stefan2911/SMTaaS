#!/usr/bin/env python3

import subprocess

from src.ev3.smt.config.config import Config

config = Config()


def call_solver(filename):
    process = subprocess.run([config.get_solver_location(), filename], check=True, stdout=subprocess.PIPE,
                             universal_newlines=True)
    output = process.stdout
    return output
