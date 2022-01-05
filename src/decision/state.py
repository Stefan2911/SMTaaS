import os

from src.config.config import Config
from src.decision.problem_classifier import get_problem_complexity
from src.monitoring.monitor import get_monitor, get_simple_monitor, SimpleMonitor

config = Config()


def _get_offload_cost(problem_size):
    return problem_size * config.get_uplink_cost() + config.get_invocation_cost()


def get_current_state(smt_problem, simple=False):
    if simple:
        monitor = get_simple_monitor()
    else:
        monitor = get_monitor()
    if smt_problem is not None:
        monitor.offload_cost = _get_offload_cost(os.stat(smt_problem).st_size / 1000)  # problem size in KB
        monitor.problem_complexity = get_problem_complexity(smt_problem)
    else:
        monitor.offload_cost = 0
        monitor.problem_complexity = 0
    return monitor


def map_detailed_state(monitor, simple=False):
    if simple:
        return SimpleMonitor(monitor)
    return monitor
