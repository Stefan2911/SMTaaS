import math
import os
from enum import Enum

from src.config.config import Config
from src.decision.problem_classifier import get_problem_complexity
from src.monitoring.monitor import get_monitor, State

config = Config()

# TODO: maybe not the most efficient solution?
MAX_RTT = config.get_max_rtt()
MAX_PROBLEM_COMPLEXITY = config.get_max_problem_complexity()


class Rating(Enum):
    poor = 0
    fair = 1
    average = 2
    good = 3
    excellent = 4


def __get_rating(value):
    if value is None:
        return Rating.poor
    number_of_rating_classes = get_number_of_rating_classes()
    converted_value = math.trunc(value * number_of_rating_classes)
    if converted_value >= number_of_rating_classes:
        converted_value = number_of_rating_classes - 1
    return Rating(number_of_rating_classes - 1 - converted_value)


def _get_offload_cost(problem_size):
    return problem_size * config.get_uplink_cost() + config.get_invocation_cost()


def get_current_state(smt_problem):
    monitor = get_monitor()
    current_state = State()
    current_state.avg_rtt_list = list(map(lambda rtt: rtt / MAX_RTT, monitor.avg_rtt_list))
    if smt_problem is not None:
        offload_cost = _get_offload_cost(os.stat(smt_problem).st_size / 1000)  # problem size in KB
        problem_complexity = get_problem_complexity(smt_problem, config.is_ev3()) / MAX_PROBLEM_COMPLEXITY
        current_state.offload_cost = offload_cost
        current_state.problem_complexity = problem_complexity
    else:
        current_state.offload_cost = 0
        current_state.problem_complexity = 0
    return current_state


def map_detailed_state(monitor, simple=False):
    if simple:
        state = State()
        state.avg_rtt_list[0] = __get_rating(monitor.avg_rtt_list[0])
        state.offload_cost = __get_rating(monitor.offload_cost)
        state.problem_complexity = __get_rating(monitor.problem_complexity)
        return state
    return monitor


def get_number_of_rating_classes():
    return len(Rating)
