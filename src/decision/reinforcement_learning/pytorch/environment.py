import logging
import time

from src.communication.rest.client import Client
from src.decision.reinforcement_learning.pytorch.config.config import Config
from src.monitoring.monitor import get_current_state

config = Config()

logging.basicConfig()
logger = logging.getLogger('environment')
logger.setLevel(level=config.get_logging_level())


class Environment:
    def __init__(self):
        self.action_space = 2
        self.state = get_current_state()
        self.test_smt_problem = "src/smt/examples/simple.smt2"
        self.basic_reward = 1
        self.client = Client()

    def get_state(self):
        return self.state

    def reset(self):
        self.state = get_current_state()

    def close(self):
        self.state = get_current_state()
        # TODO: not sure what else should be done here

    def calculate_custom_reward(self, battery_level_before_action, starting_timestamp_before_action,
                                traffic_before_action):
        reward = 0
        self.state = get_current_state()
        if config.is_mode_active('energy-aware'):
            reward += self.calculate_custom_reward_energy(battery_level_before_action)
        if config.is_mode_active('time-aware'):
            reward += self.calculate_custom_reward_time(starting_timestamp_before_action)
        if config.is_mode_active('traffic-aware'):
            reward += self.calculate_custom_reward_traffic(traffic_before_action)
        return reward

    def get_custom_reward(self, mode, difference):
        logger.debug("difference: %s", difference)
        reward_ranges = config.get_reward_ranges(mode)
        for reward_range in reward_ranges:
            if reward_range.get('start', float('-inf')) <= difference <= reward_range.get('end', float('inf')):
                return reward_range.get('reward', 0)
        return 0

    def calculate_custom_reward_energy(self, battery_level_before_action):
        battery_level_after_action = self.state.battery_level
        difference = battery_level_after_action - battery_level_before_action
        return self.get_custom_reward('energy-aware', difference)

    def calculate_custom_reward_time(self, timestamp_before_action):
        timestamp_after_action = time.time()
        difference = timestamp_after_action - timestamp_before_action
        return self.get_custom_reward('time-aware', difference)

    def calculate_custom_reward_traffic(self, traffic_before_action):
        traffic_after_action = self.state.traffic
        difference = traffic_after_action - traffic_before_action
        return self.get_custom_reward('traffic-aware', difference)

    def step(self, action):
        response = ''
        battery_level_before_action = self.state.battery_level
        timestamp_before_action = time.time()
        traffic_before_action = self.state.traffic
        if action == 1:
            logger.debug("offload")
            response = self.client.post_smt_problem_offload(self.test_smt_problem)
        elif action == 0:
            logger.debug("solve locally")
            response = self.client.post_smt_problem_local(self.test_smt_problem)
            # TODO: switch between containerized solution and direct system call
            # response = call_solver(test_file, get_solver_installation_location()))
        logger.info(response)
        return None, self.basic_reward + self.calculate_custom_reward(battery_level_before_action,
                                                                      timestamp_before_action, traffic_before_action), \
               False, None
