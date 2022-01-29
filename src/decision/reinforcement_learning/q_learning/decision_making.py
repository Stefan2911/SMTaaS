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
    q_table = np.load(q_table_location)
else:
    q_table = np.zeros((state_space_size, action_space_size))


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

    for episode in range(hyper_parameters['num-episodes']):
        environment_manager.reset()

        rewards_current_episode = 0

        for i, problem in enumerate(problems):
            smt_problem = training_problem_directory + os.sep + problem
            state = environment_manager.get_state(smt_problem)
            action = agent.select_action(map_state_to_index(state), q_table)
            reward, response = environment_manager.take_action(action, smt_problem)
            update_state_and_q_table(action, reward, state,
                                     environment_manager.get_next_smt_problem(i, problems, training_problem_directory))
            rewards_current_episode += reward

        logger.debug('episode: %s, reward: %s', episode, rewards_current_episode)

    environment_manager.close()
    persist_q_table(q_table)


def update_state_and_q_table(action, reward, state, next_smt_problem):
    next_state = environment_manager.get_state(next_smt_problem)
    update_q_table(state, action, reward, next_state)


def persist_q_table(table):
    np.save(config.get_q_table_location(), table)


def process(smt_problem):
    state = environment_manager.get_state(smt_problem)
    # exploration is only done during training
    action = agent.select_action(map_state_to_index(state), q_table, always_exploit=True)
    reward, response = environment_manager.take_action(action, smt_problem)
    # updating q table not meaningful as next state does not know problem complexity
    # next_state = environment_manager.get_state()
    # update_q_table(state, action, reward, next_state)
    return response


if __name__ == "__main__":
    training()
