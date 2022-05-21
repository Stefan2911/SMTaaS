import logging
import math
import os
from os.path import isfile

import numpy as np

from src.config.config import Config
from src.decision.reinforcement_learning.epsilon_greedy_strategy import EpsilonGreedyStrategy
from src.decision.reinforcement_learning.q_learning.agent import Agent
from src.decision.reinforcement_learning.q_learning.environment_manager import EnvironmentManager
from src.decision.state import Rating
from src.simulation.simulation import Simulation

config = Config()

logging.basicConfig()
logger = logging.getLogger('decision_making')
logger.setLevel(level=config.get_logging_level())

hyper_parameters = config.get_common_hyper_parameters()

strategy = EpsilonGreedyStrategy(hyper_parameters['eps-start'], hyper_parameters['eps-end'],
                                 hyper_parameters['eps-decay'])
environment_manager = EnvironmentManager()

agent = Agent(strategy, environment_manager.num_actions_available())

action_space_size = environment_manager.num_actions_available()
state_space_size = environment_manager.num_states_available()

simulation = Simulation.get_instance()

q_table_location = config.get_q_table_location()
if isfile(q_table_location):
    q_table = np.load(q_table_location)
else:
    q_table = np.ones((state_space_size, action_space_size))


def map_state_to_index(state):
    # e.g. (poor, poor, poor, poor, poor) = 0
    value = 0
    base = len(Rating)
    for i, s in enumerate(state):
        value += s.value * math.pow(base, i)
    return int(value)


def update_q_table(state, action, reward, new_state):
    # Update Q-table for Q(s,a)
    state_number = map_state_to_index(state)
    new_state_number = map_state_to_index(new_state)
    q_table[state_number, action] = q_table[state_number, action] * (1 - hyper_parameters['lr']) \
                                    + hyper_parameters['lr'] * \
                                    (reward + hyper_parameters['gamma'] * np.max(q_table[new_state_number, :]))


def training():
    training_problem_directory = config.get_training_problem_directory()
    problems = os.listdir(training_problem_directory)

    environment_manager.reset()

    latencies = config.get_simulation_latencies()
    for latency in latencies:
        simulation.simulate_latency(latency)
        # TODO: number of episodes must be dividable with number of possible actions
        for episode in range(hyper_parameters['num-episodes']):
            for i, problem in enumerate(problems):
                smt_problem = training_problem_directory + os.sep + problem
                state = environment_manager.get_state(smt_problem)
                # We do not want to randomly explore during training as the following effect can occur:
                # If we select one action more times than other actions and the reward is quite similar
                # (which influences the q-value) then the q-value for more times selected options
                # is automatically higher
                action = int(episode % action_space_size)
                reward, response = environment_manager.take_action(action, smt_problem)
                # next state does not influence q table, therefore state can be used as next state (gamma is 0)
                logger.info('state: %s, action: %s, reward: %s', state, action, reward)
                update_q_table(state, action, reward, state)

    environment_manager.close()
    persist_q_table(q_table)


def persist_q_table(table):
    np.save(config.get_q_table_location(), table)


def process(smt_problem):
    state = environment_manager.get_state(smt_problem)
    # exploration is only done during training
    action = agent.select_action(map_state_to_index(state), q_table, always_exploit=True)
    reward, response = environment_manager.take_action(action, smt_problem)
    # TODO: Q-Table could be updated (next state does not influence)
    return response


if __name__ == "__main__":
    training()
