from itertools import count

import torch
import torch.nn.functional as F
from torch import optim

from agent import Agent
from decision.pytorch.model import EpsilonGreedyStrategy, DQN, Experience, ReplayMemory, QValues
from environment_manager import EnvironmentManager

batch_size = 256
gamma = 0.999  # discount factor used in the Bellman equation
eps_start = 1  # starting value of epsilon (epsilon = exploration rate)
eps_end = 0.01  # ending value of epsilon
eps_decay = 0.001  # decay rate used to decay epsilon over time
target_update = 10  # defines how frequently (in terms of episodes), the target network weights are updated
memory_size = 100000  # capacity of replay memory
lr = 0.001  # learning rate
num_episodes = 100  # number of episodes

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # if cuda is selected the GPU is used
environment_manager = EnvironmentManager(device)
strategy = EpsilonGreedyStrategy(eps_start, eps_end, eps_decay)
agent = Agent(strategy, environment_manager.num_actions_available(), device)
memory = ReplayMemory(memory_size)

policy_net = DQN(environment_manager.get_number_of_indicators(), environment_manager.num_actions_available()).to(device)
target_net = DQN(environment_manager.get_number_of_indicators(), environment_manager.num_actions_available()).to(device)

target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

optimizer = optim.Adam(params=policy_net.parameters(), lr=lr)

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
    if len(memory) < batch_size:
        return
    experiences = memory.sample(batch_size)
    states, actions, rewards, next_states = extract_tensors(experiences)

    current_q_values = QValues.get_current(policy_net, states, actions)
    next_q_values = QValues.get_next(target_net, next_states)
    target_q_values = (next_q_values * gamma) + rewards

    loss = F.mse_loss(current_q_values, target_q_values.unsqueeze(1))
    optimizer.zero_grad()  # gradients of all weights and biases in policy_net are set to zero
    loss.backward()
    # updates the weights and biases with the gradients that were computed when called backward() on loss
    optimizer.step()


def training():
    for episode in range(num_episodes):
        environment_manager.reset()
        state = environment_manager.get_state()

        for timestep in count():
            action = agent.select_action(state, policy_net)
            reward = environment_manager.take_action(action)
            next_state = environment_manager.get_state()
            memory.push(Experience(state, action, next_state, reward))
            state = next_state

            optimize_model()

            if environment_manager.done:  # TODO: in our scenario never done, maybe define finite number of smt problems
                episode_durations.append(timestep)
                break

        # Update the target network, copying all weights and biases in DQN
        if episode % target_update == 0:
            target_net.load_state_dict(policy_net.state_dict())

    environment_manager.close()


if __name__ == "__main__":
    training()
