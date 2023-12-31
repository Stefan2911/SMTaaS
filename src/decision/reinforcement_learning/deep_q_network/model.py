import random
from collections import deque
from collections import namedtuple

import torch
import torch.nn as nn

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

        self.layers = nn.Sequential(
            nn.Linear(in_features=number_of_indicators, out_features=24),
            nn.BatchNorm1d(24),
            nn.LeakyReLU(),
            nn.Linear(in_features=24, out_features=24),
            nn.BatchNorm1d(24),
            nn.LeakyReLU(),
            nn.Linear(in_features=24, out_features=24),
            nn.BatchNorm1d(24),
            nn.LeakyReLU(),
            nn.Linear(24, out_features=number_of_actions)
        )

    def forward(self, t):
        return self.layers(t)


class QValues:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @staticmethod
    def get_current(policy_net, states, actions):
        return policy_net(states).gather(dim=1, index=actions.unsqueeze(-1))

    @staticmethod
    def get_next(target_net, next_states):
        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended, in our case there is no final state)
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, next_states)),
                                      device=QValues.device, dtype=torch.bool)
        batch_size = next_states.shape[0]
        values = torch.zeros(batch_size, device=QValues.device)
        values[non_final_mask] = target_net(next_states).max(1)[0].detach()
        return values
