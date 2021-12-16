import os
import sys
import time

from src.decision.processing_ev3 import process

start = time.time()
problem_directory = sys.argv[1]
iterations = sys.argv[2]
decision_mode = sys.argv[3]
for i in range(0, int(iterations)):
    for filename in os.listdir(problem_directory):
        process(problem_directory + os.sep + filename, decision_mode)
end = time.time()

print(start, end, end - start)
