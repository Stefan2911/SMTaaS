import logging
import os
import random
import sys
import time

from src.communication.client import post_smt_problem
from src.config.config import Config
from src.decision.processing_ev3 import process
from src.smt.smt_solver.native.solver import call_solver

config = Config()

logging.basicConfig()
logger = logging.getLogger('evaluation')
logger.setLevel(level=config.get_logging_level())


def print_results(start_time, end_time, problems_solved):
    time_needed = end_time - start_time
    logger.info('start time: %s, end time: %s, time needed: %s' % (time.asctime(time.localtime(start_time)),
                                                                   time.asctime(time.localtime(end_time)),
                                                                   time_needed))
    logger.info('problems solved: %s, time needed per problem: %s' % (problems_solved, (time_needed / problems_solved)))


def process_file(approach, problem_directory, filename):
    if approach == 'robot_only':
        call_solver(problem_directory + os.sep + filename)
    elif approach == 'ded_only':
        post_smt_problem(problem_directory + os.sep + filename, random.choice(config.get_ded_instances()))
    elif approach == 'cloud_only':
        post_smt_problem(problem_directory + os.sep + filename, random.choice(config.get_cloud_instances()))
    elif approach == 'q_learning':
        process(problem_directory + os.sep + filename)


def evaluate():
    problem_directories = sys.argv[4:]
    goal = sys.argv[1]
    iterations = 0
    if goal == 'time':
        iterations = int(sys.argv[2])
    approach = sys.argv[3]

    for problem_directory in problem_directories:
        problems_solved = 0

        start_time = time.time()
        if goal == 'time':
            for i in range(0, int(iterations)):
                for filename in os.listdir(problem_directory):
                    process_file(approach, problem_directory, filename)
            problems_solved = iterations * len(os.listdir(problem_directory))
        else:
            logging.error('Goal %s is currently not supported' % goal)

        end_time = time.time()

        print_results(start_time, end_time, problems_solved)


if __name__ == "__main__":
    evaluate()
