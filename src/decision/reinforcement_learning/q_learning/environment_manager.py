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

    def get_state(self):
        return self.__get_state_tuple()

    def num_states_available(self):
        return int(math.pow(get_number_of_rating_classes(), len(self.__get_state_tuple())))

    def __get_state_tuple(self):
        state = self.env.get_state()
        return [state.battery_level, state.connectivity, state.cpu_state, state.memory_state]
