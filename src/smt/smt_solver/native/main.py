#!/usr/bin/env python3
import tempfile

from flask import Flask, request

from src.config.config import Config
from src.decision.processing import process

app = Flask(__name__)

config = Config()


@app.route("/formulae", methods=["POST"])
def solve_formula():
    with tempfile.NamedTemporaryFile() as tf:
        tf.write(request.files['formula_file'].read())
        return process(tf.name, config.get_decision_mode())


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
