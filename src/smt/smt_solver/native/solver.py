#!/usr/bin/env python3

import subprocess

from src.smt.smt_solver.native.config.config import Config

config = Config()


def call_solver(filename):
    process = subprocess.run([config.get_solver_location(), filename, '--lang', 'smtlib'], check=True,
                             stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout
    return output
