import os
import subprocess
import time


def call_solver(filename):
    process = subprocess.run(["/usr/bin/cvc4", filename, '--lang', 'smtlib'],
                             check=True, stdout=subprocess.PIPE, universal_newlines=True,
                             timeout=300)  # 5 minutes
    output = process.stdout
    return output


for filename in os.listdir("src/smt/sets/evaluation/hard/"):
    start = time.time()
    try:
        output = call_solver("src/smt/sets/evaluation/hard/" + filename)
        end = time.time()
        print(filename, start, end, end - start, output)
    except subprocess.TimeoutExpired:
        end = time.time()
        print(filename, start, end, end - start, "timeout")
