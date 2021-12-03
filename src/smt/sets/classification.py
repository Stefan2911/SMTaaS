import os
import subprocess
import time


def call_solver(filename):
    process = subprocess.run(["C:\\Users\\Acer\\Desktop\\cvc4.exe", filename, '--lang', 'smtlib'],
                             check=True, stdout=subprocess.PIPE, universal_newlines=True,
                             timeout=300)  # 5 minutes
    output = process.stdout
    return output


for filename in os.listdir("C:\\Users\\Acer\\Desktop\\smt_problems"):
    start = time.time()
    try:
        output = call_solver("C:\\Users\\Acer\\Desktop\\smt_problems\\" + filename)
        end = time.time()
        print(filename, start, end, end - start, output)
    except subprocess.TimeoutExpired:
        end = time.time()
        print(filename, start, end, end - start, "timeout")
