#!/usr/bin/env python3

from flask import Flask, request
from pysmt.shortcuts import is_sat
from pysmt.smtlib.parser import SmtLibParser

app = Flask(__name__)

parser = SmtLibParser()


@app.route("/formulae", methods=["POST"])
def solve_formula():
    script = parser.get_script(request.files['formula_file'])
    formula = script.get_last_formula()
    return str(is_sat(formula))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
