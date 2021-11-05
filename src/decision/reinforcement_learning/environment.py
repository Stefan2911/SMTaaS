import logging
import os
import time

import src.monitoring.monitor
from src.communication.rest.client import Client
from src.decision.reinforcement_learning.config.config import Config
from src.ev3.smt.solver import call_solver
from src.monitoring.monitor import get_current_state, map_detailed_state

config = Config()

logging.basicConfig()
logger = logging.getLogger('environment')
logger.setLevel(level=config.get_logging_level())


def get_number_of_rating_classes():
    return src.monitoring.monitor.get_number_of_rating_classes()


class Environment:
    def __init__(self, simple=True):
        self.action_space = 2
        self.simple = simple
        self.test_smt_problem = "src/smt/examples/simple.smt2"
        self.detailed_state = get_current_state(os.stat(self.test_smt_problem).st_size)
        self.state = map_detailed_state(self.detailed_state, simple)
        self.basic_reward = 1
        self.client = Client()

    def get_state(self):
        return self.state

    def reset(self):
        self.detailed_state = get_current_state(os.stat(self.test_smt_problem).st_size)
        self.state = map_detailed_state(self.detailed_state, self.simple)

    def close(self):
        self.reset()

    def calculate_custom_reward(self, battery_level_before_action, starting_timestamp_before_action,
                                traffic_before_action):
        reward = 0
        if config.is_mode_active('energy-aware'):
            reward += self.calculate_custom_reward_energy(battery_level_before_action)
        if config.is_mode_active('time-aware'):
            reward += self.calculate_custom_reward_time(starting_timestamp_before_action)
        if config.is_mode_active('traffic-aware'):
            reward += self.calculate_custom_reward_traffic(traffic_before_action)
        return reward

    def get_custom_reward(self, mode, difference):
        reward_ranges = config.get_reward_ranges(mode)
        for reward_range in reward_ranges:
            if reward_range.get('start', float('-inf')) <= difference <= reward_range.get('end', float('inf')):
                return reward_range.get('reward', 0)
        return 0

    def calculate_custom_reward_energy(self, battery_level_before_action):
        battery_level_after_action = self.detailed_state.battery_level
        difference = battery_level_after_action - battery_level_before_action
        return self.get_custom_reward('energy-aware', difference)

    def calculate_custom_reward_time(self, timestamp_before_action):
        timestamp_after_action = time.time()
        difference = timestamp_after_action - timestamp_before_action
        return self.get_custom_reward('time-aware', difference)

    def calculate_custom_reward_traffic(self, traffic_before_action):
        traffic_after_action = self.detailed_state.traffic
        difference = traffic_after_action - traffic_before_action
        return self.get_custom_reward('traffic-aware', difference)

    def step(self, action):
        response = ''
        battery_level_before_action = self.detailed_state.battery_level
        timestamp_before_action = time.time()
        traffic_before_action = self.detailed_state.traffic
        if action == 1:
            logger.debug("offload")
            response = self.client.post_smt_problem_offload(self.test_smt_problem)
        elif action == 0:
            logger.debug("solve locally")
            if config.is_ev3():
                response = call_solver(self.test_smt_problem)
            else:
                response = self.client.post_smt_problem_local(self.test_smt_problem)
        logger.info(response)
        logger.debug(os.stat(self.test_smt_problem).st_size)
        self.detailed_state = get_current_state(os.stat(self.test_smt_problem).st_size)
        self.state = map_detailed_state(self.detailed_state, self.simple)
        return None, self.basic_reward + self.calculate_custom_reward(battery_level_before_action,
                                                                      timestamp_before_action, traffic_before_action), \
               False, None
