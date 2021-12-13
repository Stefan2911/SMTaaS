import os
import sys
import time

from src.smt.smt_solver.native.solver import call_solver

start = time.time()
problem_directory = sys.argv[1]
iterations = sys.argv[2]
for i in range(0, int(iterations)):
    for filename in os.listdir(problem_directory):
        call_solver(problem_directory + os.sep + filename)
end = time.time()

print(start, end, end - start)
