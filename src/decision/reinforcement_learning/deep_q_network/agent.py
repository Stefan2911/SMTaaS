import random

import torch


def exploit(state, policy_net, device):
    with torch.no_grad():
        return policy_net(state).argmax(dim=1).to(device)


def explore(num_actions, device):
    offload = random.getrandbits(1)  # randomly select between offload and solve locally
    if offload:  # if offload is selected, select randomly between offload options
        action = random.randrange(1, num_actions)
        return torch.tensor([action]).to(device)
    else:
        return torch.tensor([0]).to(device)


class Agent:
    def __init__(self, strategy, num_actions, device):
        self.current_step = 0
        self.strategy = strategy
        self.num_actions = num_actions
        self.device = device

    def select_action(self, state, policy_net, always_exploit=False):
        rate = self.strategy.get_exploration_rate(self.current_step)
        self.current_step += 1

        if always_exploit:
            return exploit(state, policy_net, self.device)
        else:
            if rate > random.random():
                return explore(self.num_actions, self.device)
            else:
                return exploit(state, policy_net, self.device)
