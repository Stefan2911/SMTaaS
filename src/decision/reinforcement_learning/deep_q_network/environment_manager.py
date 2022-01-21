import torch

from src.decision.reinforcement_learning.environment import Environment


class EnvironmentManager:
    def __init__(self, device):
        self.device = device
        self.env = Environment(False)
        self.env.reset()
        self.done = False

    def reset(self):
        self.env.reset()

    def close(self):
        self.env.close()

    def num_actions_available(self):
        return self.env.action_space

    def take_action(self, action, smt_problem):
        reward, self.done, response = self.env.step(action.item(), smt_problem)
        return torch.tensor([reward], device=self.device), response

    def get_state(self, smt_problem):
        return torch.Tensor([self.__get_state_tuple(smt_problem)], device=self.device)

    def __get_state_tuple(self, smt_problem):
        state = self.env.get_state(smt_problem)
        return [state.avg_rtt, state.cpu_usage, state.memory_usage, state.problem_complexity]

    def get_number_of_indicators(self):
        return len(self.__get_state_tuple(None))

    def get_next_smt_problem(self, current_index, problems, path):
        return self.env.get_next_smt_problem(current_index, problems, path)
