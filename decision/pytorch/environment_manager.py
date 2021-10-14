import torch

from decision.pytorch.environment import Environment


class EnvironmentManager():
    def __init__(self, device):
        self.device = device
        self.env = Environment()
        self.env.reset()
        self.done = False

    def reset(self):
        self.env.reset()

    def close(self):
        self.env.close()

    def num_actions_available(self):
        return self.env.action_space

    def take_action(self, action):
        _, reward, self.done, _ = self.env.step(action.item())
        return torch.tensor([reward], device=self.device)

    def get_state(self):
        state = self.env.get_state()
        return torch.Tensor([[state.battery_level, state.avg_rtt, state.cpu_usage, state.memory_usage]],
                            device=self.device)

    def get_number_of_indicators(self):
        return self.env.get_number_of_indicators()
