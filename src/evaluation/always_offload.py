import sys
import time
import os
import random

from src.communication.rest.client import post_smt_problem

offload_instances = ["http://10.0.0.13:5000/formulae", "http://10.0.0.16:5000/formulae"]

start = time.time()
problem_directory = sys.argv[1]
for filename in os.listdir(problem_directory):
    post_smt_problem(problem_directory + os.sep + filename, random.choice(offload_instances))
end = time.time()

print(start, end, end - start)
