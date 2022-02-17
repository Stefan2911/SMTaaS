import logging
import os
from os.path import isfile

import torch
import torch.nn.functional as F
from torch import optim

from src.config.config import Config
from src.decision.reinforcement_learning.deep_q_network.agent import Agent
from src.decision.reinforcement_learning.deep_q_network.environment_manager import EnvironmentManager
from src.decision.reinforcement_learning.deep_q_network.model import DQN, Experience, ReplayMemory, QValues
from src.decision.reinforcement_learning.epsilon_greedy_strategy import EpsilonGreedyStrategy
from src.simulation.simulation import Simulation

config = Config()

logging.basicConfig()
logger = logging.getLogger('decision_making')
logger.setLevel(level=config.get_logging_level())

hyper_parameters = config.get_common_hyper_parameters()
dqn_hyper_parameters = config.get_dqn_hyper_parameters()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # if cuda is selected the GPU is used
environment_manager = EnvironmentManager(device)
strategy = EpsilonGreedyStrategy(hyper_parameters['eps-start'], hyper_parameters['eps-end'],
                                 hyper_parameters['eps-decay'])
agent = Agent(strategy, environment_manager.num_actions_available(), device)

memory = ReplayMemory(dqn_hyper_parameters['memory-size'])
number_of_indicators = environment_manager.get_number_of_indicators()
number_of_actions = environment_manager.num_actions_available()

neural_network_location = config.get_neural_network_location()

policy_net = DQN(number_of_indicators, number_of_actions).to(device)
target_net = DQN(number_of_indicators, number_of_actions).to(device)

if isfile(neural_network_location):
    policy_net.load_state_dict(torch.load(neural_network_location))

target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

# default learning rate is used lr = 0.001
optimizer = optim.Adam(params=policy_net.parameters())


def extract_tensors(experiences):
    # Convert batch of Experiences to Experience of batches
    batch = Experience(*zip(*experiences))

    t1 = torch.cat(batch.state)
    t2 = torch.cat(batch.action)
    t3 = torch.cat(batch.reward)
    t4 = torch.cat(batch.next_state)

    return t1, t2, t3, t4


def optimize_model():
    if len(memory) < dqn_hyper_parameters['batch-size']:
        return
    experiences = memory.sample(dqn_hyper_parameters['batch-size'])
    states, actions, rewards, next_states = extract_tensors(experiences)

    current_q_values = QValues.get_current(policy_net, states, actions)
    target_q_values = rewards
    logger.info('difference: %s', torch.sum(torch.abs(current_q_values.squeeze(1) - target_q_values)))

    # l1_loss = MEA = mean absolute error
    loss = F.l1_loss(current_q_values, target_q_values.unsqueeze(1))
    optimizer.zero_grad()  # gradients of all weights and biases in policy_net are set to zero
    loss.backward()
    # updates the weights and biases with the gradients that were computed when called backward() on loss
    optimizer.step()


simulation = Simulation.get_instance()


def training():
    training_problem_directory = config.get_training_problem_directory()
    problems = os.listdir(training_problem_directory)

    environment_manager.reset()
    for episode in range(hyper_parameters['num-episodes']):
        rewards_current_episode = 0

        for i, problem in enumerate(problems):
            simulation.simulate_random_latency()
            smt_problem = training_problem_directory + os.sep + problem
            state = environment_manager.get_state(smt_problem)
            action = agent.select_action(state, policy_net)
            reward, response = environment_manager.take_action(action, smt_problem)
            rewards_current_episode += reward.item()
            # next state does not influence training
            next_state = state
            experience = Experience(state, action, next_state, reward)
            logger.info('episode: %s, experience: %s', episode, experience)
            memory.push(experience)

            optimize_model()

        logger.debug('episode: %s, reward: %s', episode, rewards_current_episode)

        # Update the target network, copying all weights and biases in DQN
        if episode % dqn_hyper_parameters['target-update'] == 0:
            logger.debug('update target network')
            target_net.load_state_dict(policy_net.state_dict())

    target_net.load_state_dict(policy_net.state_dict())
    environment_manager.close()
    torch.save(target_net.state_dict(), neural_network_location)


def process(smt_problem):
    state = environment_manager.get_state(smt_problem)
    # exploration is only done during training
    action = agent.select_action(state, target_net, always_exploit=True)
    reward, response = environment_manager.take_action(action, smt_problem)
    logger.debug("state: %s, action: %s, reward: %s", state, action, reward)
    # TODO: DQN could be updated (next state does not influence)
    return response


if __name__ == "__main__":
    training()
