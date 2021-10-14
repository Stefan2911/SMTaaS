from itertools import count

import torch
import torch.nn.functional as F
from torch import optim

from src.decision.reinforcement_learning.pytorch.agent import Agent
from src.decision.reinforcement_learning.pytorch.config.config import Config
from src.decision.reinforcement_learning.pytorch.environment_manager import EnvironmentManager
from src.decision.reinforcement_learning.pytorch.model import EpsilonGreedyStrategy, DQN, Experience, ReplayMemory, \
    QValues

config = Config()

hyper_parameters = config.get_hyper_parameters()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # if cuda is selected the GPU is used
environment_manager = EnvironmentManager(device)
strategy = EpsilonGreedyStrategy(hyper_parameters['eps-start'], hyper_parameters['eps-end'],
                                 hyper_parameters['eps-decay'])
agent = Agent(strategy, environment_manager.num_actions_available(), device)
memory = ReplayMemory(hyper_parameters['memory-size'])

policy_net = DQN(environment_manager.get_number_of_indicators(), environment_manager.num_actions_available()).to(device)
target_net = DQN(environment_manager.get_number_of_indicators(), environment_manager.num_actions_available()).to(device)

target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(params=policy_net.parameters(), lr=hyper_parameters['lr'])

episode_durations = []


def extract_tensors(experiences):
    # Convert batch of Experiences to Experience of batches
    batch = Experience(*zip(*experiences))

    t1 = torch.cat(batch.state)
    t2 = torch.cat(batch.action)
    t3 = torch.cat(batch.reward)
    t4 = torch.cat(batch.next_state)

    return t1, t2, t3, t4


def optimize_model():
    if len(memory) < hyper_parameters['batch-size']:
        return
    experiences = memory.sample(hyper_parameters['batch-size'])
    states, actions, rewards, next_states = extract_tensors(experiences)

    current_q_values = QValues.get_current(policy_net, states, actions)
    next_q_values = QValues.get_next(target_net, next_states)
    target_q_values = (next_q_values * hyper_parameters['gamma']) + rewards

    loss = F.mse_loss(current_q_values, target_q_values.unsqueeze(1))
    optimizer.zero_grad()  # gradients of all weights and biases in policy_net are set to zero
    loss.backward()
    # updates the weights and biases with the gradients that were computed when called backward() on loss
    optimizer.step()


def training():
    for episode in range(hyper_parameters['num-episodes']):
        environment_manager.reset()
        state = environment_manager.get_state()

        for time_step in count():
            action = agent.select_action(state, policy_net)
            reward = environment_manager.take_action(action)
            next_state = environment_manager.get_state()
            memory.push(Experience(state, action, next_state, reward))
            state = next_state

            optimize_model()

            if environment_manager.done:  # TODO: in our scenario never done, maybe define finite number of smt problems
                episode_durations.append(time_step)
                break

        # Update the target network, copying all weights and biases in DQN
        if episode % hyper_parameters['target-update'] == 0:
            target_net.load_state_dict(policy_net.state_dict())

    environment_manager.close()


if __name__ == "__main__":
    training()
