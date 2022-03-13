import random

import numpy as np


def exploit(q_table, state_index):
    return np.argmax(q_table[state_index, :])


def explore(num_actions):
    return random.randrange(0, num_actions)  # randomly select between offload options and solve locally


class Agent:
    def __init__(self, strategy, num_actions):
        self.current_step = 0
        self.strategy = strategy
        self.num_actions = num_actions

    def select_action(self, state_index, q_table, always_exploit=False):
        rate = self.strategy.get_exploration_rate(self.current_step)
        self.current_step += 1

        if always_exploit:
            return exploit(q_table, state_index)
        else:
            if rate > random.random():
                return explore(self.num_actions)
            else:
                return exploit(q_table, state_index)
