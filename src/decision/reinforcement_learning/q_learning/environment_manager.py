import math

from src.decision.reinforcement_learning.environment import Environment, get_number_of_rating_classes


class EnvironmentManager:
    def __init__(self):
        self.env = Environment()
        self.env.reset()
        self.done = False

    def reset(self):
        self.env.reset()

    def close(self):
        self.env.close()

    def num_actions_available(self):
        return self.env.action_space

    def take_action(self, action, smt_problem):
        reward, self.done, response = self.env.step(action, smt_problem)
        return reward, response

    def get_state(self, smt_problem):
        return self.__get_state_tuple(smt_problem)

    def num_states_available(self):
        return int(math.pow(get_number_of_rating_classes(), len(self.__get_state_tuple(None))))

    def __get_state_tuple(self, smt_problem):
        state = self.env.get_state(smt_problem)
        return [state.connectivity, state.problem_complexity]

    def get_next_smt_problem(self, current_index, problems, path):
        return self.env.get_next_smt_problem(current_index, problems, path)
