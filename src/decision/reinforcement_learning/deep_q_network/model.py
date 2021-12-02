import random
from collections import deque
from collections import namedtuple

import torch
import torch.nn as nn
import torch.nn.functional as F

Experience = namedtuple(
    'Experience',
    ('state', 'action', 'next_state', 'reward')
)


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, experience):
        self.memory.append(experience)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    def __init__(self, number_of_indicators, number_of_actions):
        super().__init__()

        # TODO: fine tuning of neural network structure
        # the following links shows some rules of thumb:
        # https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw
        # https://towardsdatascience.com/beginners-ask-how-many-hidden-layers-neurons-to-use-in-artificial-neural-networks-51466afa0d3e
        # Results:
        # number of hidden layer: in most cases one hidden layer is sufficient
        # number of neurons in hidden layer: we use the following rule:
        # 2/3 the size of the input layer + size of output layer
        # = 2/3 * 4 + 2 = 4.666 = 5

        self.fc1 = nn.Linear(in_features=number_of_indicators, out_features=5)
        self.out = nn.Linear(in_features=5, out_features=number_of_actions)

    def forward(self, t):
        t = F.relu(self.fc1(t))
        t = self.out(t)
        return t


class QValues:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @staticmethod
    def get_current(policy_net, states, actions):
        return policy_net(states).gather(dim=1, index=actions.unsqueeze(-1))

    @staticmethod
    def get_next(target_net, next_states):
        # In our scenario there does not exist any final state, therefore we check if the state value is -1 which
        # is not possible to mask any state as non final states
        final_state_locations = next_states.flatten(start_dim=1).max(dim=1)[0].eq(-1).type(torch.bool)
        non_final_state_locations = (final_state_locations is False)
        non_final_states = next_states[non_final_state_locations]
        batch_size = next_states.shape[0]
        values = torch.zeros(batch_size).to(QValues.device)
        values[non_final_state_locations] = target_net(non_final_states).max(dim=1)[0].detach()
        return values
