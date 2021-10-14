import logging
import time

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

    def calculate_custom_reward_battery_level(self, battery_level_before_action):
        battery_level_after_action = self.state.battery_level
        difference = battery_level_after_action - battery_level_before_action
        logger.debug("difference: %s", difference)
        # TODO: fine tuning necessary
        if difference == 0:
            return 5
        if difference == 1:
            return 2
        if difference > 5:
            return -2

    def calculate_custom_reward_fastness(self, starting_timestamp):
        current_timestamp = time.time()
        difference = current_timestamp - starting_timestamp
        # TODO: fine tuning necessary
        if difference < 5:
            return 5
        if difference < 10:
            return 2
        if difference > 20:
            return -2

    def step(self, action):
        response = ''
        battery_level_before_action = self.state.battery_level
        if action == 1:
            logger.debug("offload")
            response = post_smt_problem(self.test_smt_problem, self.api_url)
        elif action == 0:
            logger.debug("solve locally")
            response = post_smt_problem(self.test_smt_problem, 'http://127.0.0.1:5000/formulae')
            # TODO: switch between containerized solution and direct system call
            # response = call_solver(test_file, get_solver_installation_location()))
        logger.info(response)
        return None, self.basic_reward + self.calculate_custom_reward_battery_level(battery_level_before_action), \
               False, None
