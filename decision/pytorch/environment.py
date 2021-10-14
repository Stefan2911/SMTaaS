import logging
import time

from decision.pytorch.config import get_reward_ranges, is_mode_active
from ev3.communication.rest.client import post_smt_problem
from monitoring.monitor import get_current_state

logging.basicConfig()
logger = logging.getLogger('environment')
logger.setLevel(level=logging.DEBUG)


class Environment:
    def __init__(self):
        self.action_space = 2
        self.state = get_current_state()
        self.test_smt_problem = "./simple.smt2"
        self.api_url = 'http://10.0.0.13:5000/formulae'
        self.basic_reward = 1

    def get_state(self):
        return self.state

    def reset(self):
        self.state = get_current_state()

    def close(self):
        self.state = get_current_state()
        # TODO: not sure what else should be done here

    def get_number_of_indicators(self):
        return 4  # TODO: configurable etc.

    def calculate_custom_reward(self, battery_level_before_action, starting_timestamp_before_action):
        reward = 0
        if is_mode_active('energy-efficient'):
            reward += self.calculate_custom_reward_battery_level(battery_level_before_action)
        if is_mode_active('fastness'):
            reward += self.calculate_custom_reward_fastness(starting_timestamp_before_action)
        if is_mode_active('less-network-traffic'):
            reward += self.calculate_custom_reward_less_network_traffic()
        return reward

    def get_custom_reward(self, mode, difference):
        logger.debug("difference: %s", difference)
        reward_ranges = get_reward_ranges(mode)
        for reward_range in reward_ranges:
            if reward_range.get('start', float('-inf')) <= difference <= reward_range.get('end', float('inf')):
                return reward_range.get('reward', 0)

    def calculate_custom_reward_battery_level(self, battery_level_before_action):
        battery_level_after_action = self.state.battery_level
        difference = battery_level_after_action - battery_level_before_action
        return self.get_custom_reward('energy-efficient', difference)

    def calculate_custom_reward_fastness(self, starting_timestamp):
        current_timestamp = time.time()
        difference = current_timestamp - starting_timestamp
        return self.get_custom_reward('fastness', difference)

    def calculate_custom_reward_less_network_traffic(self):
        return 0  # TODO

    def step(self, action):
        response = ''
        battery_level_before_action = self.state.battery_level
        timestamp_before_action = time.time()
        if action == 1:
            logger.debug("offload")
            response = post_smt_problem(self.test_smt_problem, self.api_url)
        elif action == 0:
            logger.debug("solve locally")
            response = post_smt_problem(self.test_smt_problem, 'http://127.0.0.1:5000/formulae')
            # TODO: switch between containerized solution and direct system call
            # response = call_solver(test_file, get_solver_installation_location()))
        logger.info(response)
        return None, self.basic_reward + self.calculate_custom_reward(battery_level_before_action,
                                                                      timestamp_before_action), \
               False, None
