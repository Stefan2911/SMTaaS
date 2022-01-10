import random

import numpy as np


def exploit(q_table, state_index):
    return np.argmax(q_table[state_index, :])


def explore(num_actions):
    offload = random.getrandbits(1)  # randomly select between offload and solve locally
    if offload:  # if offload is selected, select randomly between offload options
        return random.randrange(1, num_actions)
    else:
        return 0


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
