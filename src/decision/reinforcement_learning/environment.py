import logging
import os
import time
from enum import Enum

import src.monitoring.monitor
from src.communication.client import post_smt_problem
from src.config.config import Config
from src.decision.state import map_detailed_state, get_current_state
from src.smt.smt_solver.native.solver import call_solver


class RewardMode(Enum):
    time_aware = "time-aware"
    traffic_aware = "traffic-aware"


config = Config()

logging.basicConfig()
logger = logging.getLogger('environment')
logger.setLevel(level=config.get_logging_level())


def get_number_of_rating_classes():
    return src.monitoring.monitor.get_number_of_rating_classes()


def _offload(action, smt_problem):
    logger.debug("offload")
    response = post_smt_problem(smt_problem, config.get_solver_instance(action - 1))
    return response


def _solve_locally(smt_problem):
    logger.debug("solve locally")
    if config.is_native_solver():
        response = call_solver(smt_problem)
    else:
        response = post_smt_problem(smt_problem, 'http://127.0.0.1:5000/formulae')
    return response


def _get_custom_reward(mode, difference):
    reward_ranges = config.get_reward_ranges(mode)
    for reward_range in reward_ranges:
        if reward_range.get('start', float('-inf')) <= difference < reward_range.get('end', float('inf')):
            return reward_range.get('reward', 0)
    return 0


def _handle_action(action, smt_problem):
    # 0 is solving locally, 1 is first available instance to offload, 2 is second available instance and so on
    if action == 0:
        response = _solve_locally(smt_problem)
    else:
        response = _offload(action, smt_problem)
    return response


def _calculate_custom_reward_time(timestamp_before_action):
    timestamp_after_action = time.time()
    difference = timestamp_after_action - timestamp_before_action
    # TODO: call _get_custom_reward, if configuration is used
    time_reward = 3 - difference
    return time_reward


def _calculate_custom_reward(starting_timestamp_before_action):
    reward = 0
    if config.is_mode_active(RewardMode.time_aware):
        reward += _calculate_custom_reward_time(starting_timestamp_before_action)
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
        timestamp_before_action = time.time()
        response = _handle_action(action, smt_problem)
        return _calculate_custom_reward(timestamp_before_action), False, response

    def update_state(self, smt_problem):
        self.detailed_state = get_current_state(smt_problem)
        self.state = map_detailed_state(self.detailed_state, self.simple)

    def get_next_smt_problem(self, current_index, problems, path):
        if current_index == len(problems):
            return path + os.sep + problems[0]
        else:
            return path + os.sep + problems[++current_index]
