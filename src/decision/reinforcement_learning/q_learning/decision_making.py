import logging
import math
import os
from os.path import isfile

import numpy as np

from src.config.config import Config
from src.decision.reinforcement_learning.epsilon_greedy_strategy import EpsilonGreedyStrategy
from src.decision.reinforcement_learning.q_learning.agent import Agent
from src.decision.reinforcement_learning.q_learning.environment_manager import EnvironmentManager
from src.monitoring.monitor import Rating

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

q_table_location = config.get_q_table_location()
if isfile(q_table_location):
    q_table = np.load(q_table_location).reshape(state_space_size, action_space_size)
else:
    q_table = np.zeros((state_space_size, action_space_size))


def map_state_to_index(state):
    # e.g. (poor, poor, poor, poor) = 0
    value = 0
    for i, s in enumerate(state):
        value += s.value * math.pow(len(Rating), i)
    return int(value)


def update_q_table(state, action, reward, new_state):
    # Update Q-table for Q(s,a)
    state_number = map_state_to_index(state)
    new_state_number = map_state_to_index(new_state)
    q_table[state_number, action] = q_table[state_number, action] * (1 - hyper_parameters['lr']) + hyper_parameters[
        'lr'] * \
                                    (reward + hyper_parameters['gamma'] * np.max(q_table[new_state_number, :]))


def training():
    training_problem_directory = config.get_training_problem_directory()

    for episode in range(hyper_parameters['num-episodes']):
        environment_manager.reset()
        state = environment_manager.get_state()

        rewards_current_episode = 0

        for filename in os.listdir(training_problem_directory):
            action = agent.select_action(map_state_to_index(state), q_table)
            reward, response = environment_manager.take_action(action, training_problem_directory + os.sep + filename)
            next_state = environment_manager.get_state()
            update_q_table(state, action, reward, next_state)
            rewards_current_episode += reward
            state = next_state

        logger.debug('episode: %s, reward: %s', episode, rewards_current_episode)

    environment_manager.close()
    persist_q_table(q_table)


def persist_q_table(table):
    np.save(config.get_q_table_location(), table)


def process(smt_problem):
    state = environment_manager.get_state()
    action = agent.select_action(map_state_to_index(state), q_table)
    reward, response = environment_manager.take_action(action, smt_problem)
    next_state = environment_manager.get_state()
    update_q_table(state, action, reward, next_state)
    return response


if __name__ == "__main__":
    training()
