import os
import random
import sys
import time

from src.communication.rest.client import post_smt_problem

# cloud
# offload_instances = ["http://194.182.171.9:5000/formulae"]

# DeDs
offload_instances = ["http://10.0.0.13:5000/formulae", "http://10.0.0.16:5000/formulae"]

start = time.time()
problem_directory = sys.argv[1]
iterations = sys.argv[2]
for i in range(0, int(iterations)):
    for filename in os.listdir(problem_directory):
        post_smt_problem(problem_directory + os.sep + filename, random.choice(offload_instances))
end = time.time()

print(start, end, end - start)
