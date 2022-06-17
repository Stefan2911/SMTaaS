import logging
import os
import random
import time

from src.communication.client import post_smt_problem
from src.config.config import Config
from src.decision.decision_mode import DecisionMode
from src.decision.processing_ev3 import process
from src.evaluation.evaluation_common import print_results, get_setup
from src.smt.smt_solver.native.solver import call_solver

config = Config()

logging.basicConfig()
logger = logging.getLogger('evaluation')
logger.setLevel(level=config.get_logging_level())


def process_file(approach, problem_directory, filename):
    if approach == 'robot_only':
        call_solver(problem_directory + os.sep + filename)
    elif approach == 'ded_only':
        post_smt_problem(problem_directory + os.sep + filename, random.choice(config.get_edge_instances()))
    elif approach == 'cloud_only':
        post_smt_problem(problem_directory + os.sep + filename, random.choice(config.get_cloud_instances()))
    elif approach == 'q_learning':
        process(problem_directory + os.sep + filename, decision_mode=DecisionMode.q_learning)


def evaluate():
    problem_directories, goal, iterations, approach, simulation, simulated_latencies = get_setup()

    for problem_directory in problem_directories:
        logger.info('set: %s', problem_directory)

        for simulated_latency in simulated_latencies:
            logger.info('additional latency: %s', simulated_latency)
            simulation.simulate_latency(simulated_latency)
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
