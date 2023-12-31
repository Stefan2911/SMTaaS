import datetime
import logging
from enum import Enum

from src.communication.client import post_smt_problem
from src.config.config import Config
from src.decision.state import map_detailed_state, get_current_state, get_number_of_rating_classes
from src.simulation.simulation import Simulation
from src.smt.smt_solver.native.solver import call_solver


class RewardMode(Enum):
    time_aware = "time-aware"
    energy_aware = "energy-aware"


config = Config()

logging.basicConfig()
logger = logging.getLogger('environment')
logger.setLevel(level=config.get_logging_level())

simulation = Simulation.get_instance()

MAX_TIME = 4
MAX_ENERGY = 1

LOCALLY_ENERGY_COST_FACTOR = 1.0
OFFLOAD_ENERGY_COST_FACTOR = 1.0


def get_rating_classes():
    return get_number_of_rating_classes()


def _offload(solver_instance, smt_problem):
    logger.debug("offload")
    response = post_smt_problem(smt_problem, solver_instance)
    return response


def _solve_locally(smt_problem):
    logger.debug("solve locally")
    response = call_solver(smt_problem)
    return response

def _calculate_custom_reward_time(timestamp_before_action):
    timestamp_after_action = datetime.datetime.now()
    difference = timestamp_after_action - timestamp_before_action
    time_reward = MAX_TIME - difference.total_seconds()
    return time_reward


def _calculate_custom_reward_energy(state, action):
    if action == 0:
        return MAX_ENERGY - state.problem_complexity * LOCALLY_ENERGY_COST_FACTOR
    return MAX_ENERGY - state.offload_cost * OFFLOAD_ENERGY_COST_FACTOR


def _calculate_custom_reward(starting_timestamp_before_action, state, action):
    reward = 0
    if config.is_mode_active(RewardMode.time_aware):
        reward += _calculate_custom_reward_time(starting_timestamp_before_action)
    if config.is_mode_active(RewardMode.energy_aware):
        reward += _calculate_custom_reward_energy(state, action)
    return reward


class Environment:
    def __init__(self, simple=True):
        self.action_space = config.get_action_space()
        self.simple = simple
        self.detailed_state = get_current_state(None)
        self.state = map_detailed_state(self.detailed_state, simple)

    def get_state(self, smt_problem):
        self.update_state(smt_problem)
        return self.state

    def reset(self):
        self.update_state(None)

    def close(self):
        self.reset()

    def step(self, action, smt_problem):
        timestamp_before_action = datetime.datetime.now()
        # 0 is solving locally, 1 is first available instance to offload, 2 is second available instance and so on
        if action == 0:
            response = _solve_locally(smt_problem)
        else:
            solver_instance = config.get_solver_instance(action - 1)
            waiting_time = simulation.get_additional_waiting_time()
            timestamp_before_action = timestamp_before_action - waiting_time
            response = _offload(solver_instance, smt_problem)

        return _calculate_custom_reward(timestamp_before_action, self.detailed_state, action), False, response

    def update_state(self, smt_problem):
        self.detailed_state = get_current_state(smt_problem)
        self.state = map_detailed_state(self.detailed_state, self.simple)
