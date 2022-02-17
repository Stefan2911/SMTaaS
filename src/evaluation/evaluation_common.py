import logging
import sys
import time

from src.config.config import Config
from src.simulation.simulation import Simulation

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


def get_setup():
    problem_directories = sys.argv[4:]
    goal = sys.argv[1]
    iterations = 0
    if goal == 'time':
        iterations = int(sys.argv[2])
    approach = sys.argv[3]

    simulation = Simulation.get_instance()

    simulated_latencies = [0, 100, 200, 300, 400]

    return problem_directories, goal, iterations, approach, simulation, simulated_latencies
