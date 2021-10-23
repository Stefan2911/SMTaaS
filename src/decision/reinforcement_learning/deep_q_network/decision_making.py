import logging
from itertools import count

import torch
import torch.nn.functional as F
from torch import optim

from src.decision.reinforcement_learning.deep_q_network.agent import Agent
from src.decision.reinforcement_learning.deep_q_network.config.config import Config
from src.decision.reinforcement_learning.deep_q_network.environment_manager import EnvironmentManager
from src.decision.reinforcement_learning.deep_q_network.model import DQN, Experience, ReplayMemory, QValues
from src.decision.reinforcement_learning.epsilon_greedy_strategy import EpsilonGreedyStrategy

config = Config()

logging.basicConfig()
logger = logging.getLogger('decision_making')
logger.setLevel(level=config.get_logging_level())

hyper_parameters = config.get_hyper_parameters()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # if cuda is selected the GPU is used
environment_manager = EnvironmentManager(device)
strategy = EpsilonGreedyStrategy(hyper_parameters['eps-start'], hyper_parameters['eps-end'],
                                 hyper_parameters['eps-decay'])
agent = Agent(strategy, environment_manager.num_actions_available(), device)
memory = ReplayMemory(hyper_parameters['memory-size'])

number_of_indicators = environment_manager.get_number_of_indicators()
number_of_actions = environment_manager.num_actions_available()
policy_net = DQN(number_of_indicators, number_of_actions).to(device)
target_net = DQN(number_of_indicators, number_of_actions).to(device)

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

    # mse = mean squared error
    loss = F.mse_loss(current_q_values, target_q_values.unsqueeze(1))
    optimizer.zero_grad()  # gradients of all weights and biases in policy_net are set to zero
    loss.backward()
    # updates the weights and biases with the gradients that were computed when called backward() on loss
    optimizer.step()


def training():
    for episode in range(hyper_parameters['num-episodes']):
        environment_manager.reset()
        state = environment_manager.get_state()

        rewards_current_episode = 0

        for time_step in count():
            action = agent.select_action(state, policy_net)
            reward = environment_manager.take_action(action)
            rewards_current_episode += reward.item()
            next_state = environment_manager.get_state()
            memory.push(Experience(state, action, next_state, reward))
            state = next_state

            optimize_model()

            # in our scenario done is never reached, therefore we need to define a episode length
            if environment_manager.done or time_step == hyper_parameters['episode-length']:
                episode_durations.append(time_step)
                break

        logger.debug('episode: %s, reward: %s', episode, rewards_current_episode)

        # Update the target network, copying all weights and biases in DQN
        if episode % hyper_parameters['target-update'] == 0:
            logger.debug('update target network')
            target_net.load_state_dict(policy_net.state_dict())

    environment_manager.close()


if __name__ == "__main__":
    training()
