import os
import random
import sys
import time

from src.communication.client import post_smt_problem
from src.config.config import Config
from src.decision.processing_ev3 import process
from src.monitoring.monitor_battery_level_ev3 import get_battery_level_ev3
from src.smt.smt_solver.native.solver import call_solver

config = Config()


def print_results(start_time, end_time, start_battery_level, end_battery_level, problems_solved):
    print('start time: %s, end time: %s, time needed: %s' % (start_time, end_time, end_time - start_time))
    print('battery level start: %s, battery level end: %s' % (start_battery_level, end_battery_level))
    print('problems solved: ', problems_solved)


def process_file(approach, problem_directory, filename):
    if approach == 'robot_only':
        call_solver(problem_directory + os.sep + filename)
    elif approach == 'ded_only':
        post_smt_problem(problem_directory + os.sep + filename, random.choice(config.get_ded_instances()))
    elif approach == 'cloud_only':
        post_smt_problem(problem_directory + os.sep + filename, random.choice(config.get_cloud_instances()))
    elif approach == 'q_learning':
        process(problem_directory + os.sep + filename, 'q_learning')


def evaluate():
    problem_directory = sys.argv[1]
    goal = sys.argv[2]
    unload_percentage = 0
    iterations = 0
    if goal == 'energy':
        unload_percentage = float(sys.argv[3])
    elif goal == 'time':
        iterations = int(sys.argv[3])
    approach = sys.argv[4]

    start_battery_level = get_battery_level_ev3()
    end_battery_level = start_battery_level - float(unload_percentage)
    problems_solved = 0

    start_time = time.time()
    if goal == 'energy':
        files = os.listdir(problem_directory)
        file_index = 0

        while (get_battery_level_ev3() - end_battery_level) > 0:
            process_file(approach, problem_directory, files[file_index])
            file_index += 1
            if file_index >= len(files):
                file_index = 0
            problems_solved += 1
    elif goal == 'time':
        for i in range(0, int(iterations)):
            for filename in os.listdir(problem_directory):
                process_file(approach, problem_directory, filename)
        problems_solved = iterations * len(os.listdir(problem_directory))

    end_time = time.time()
    end_battery_level = get_battery_level_ev3()

    print_results(start_time, end_time, start_battery_level, end_battery_level, problems_solved)


if __name__ == "__main__":
    evaluate()
