import os

from src.config.config import Config
from src.decision.problem_classifier import get_problem_complexity
from src.monitoring.monitor import get_monitor, SimpleMonitor, get_rating

config = Config()


def _get_offload_cost(problem_size):
    return problem_size * config.get_uplink_cost() + config.get_invocation_cost()


def get_current_state(smt_problem):
    monitor = get_monitor()
    if smt_problem is not None:
        offload_cost = _get_offload_cost(os.stat(smt_problem).st_size / 1000)  # problem size in KB
        problem_complexity = get_problem_complexity(smt_problem)
        monitor.offload_cost = offload_cost
        monitor.problem_complexity = problem_complexity
    else:
        monitor.offload_cost = 0
        monitor.problem_complexity = 0
    return monitor


def map_detailed_state(monitor, simple=False):
    if simple:
        state = SimpleMonitor(monitor)
        state.offload_cost = get_rating(monitor.offload_cost, config.get_indicator_ranges('offload-cost'))
        state.problem_complexity = get_rating(monitor.problem_complexity,
                                              config.get_indicator_ranges('problem-complexity'))
        return state
    return monitor
