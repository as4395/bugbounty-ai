# Purpose: Define the Deep Q-Learning agent using a neural network, with training logic,
# and experience replay, model saving/loading, and action selection using the epsilon-greedy strategy.

import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque

# Requirements:
# ```bash
# pip install torchvision
#
# ```bash
# pip3 install torchvision
#
# ```bash
# pip install numpy
#
# ```bash
# pip3 install numpy


class DQN(nn.Module):
    # A simple feedforward neural network for approximating Q-values.
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )

    def forward(self, x):
        return self.net(x)


class DQNAgent:
    """
    Deep Q-Learning agent with experience replay, target network, and epsilon-greedy strategy.
    Trains a PyTorch model to learn optimal actions from state transitions.
    """
    def __init__(self, state_dim, action_dim):
        self.model = DQN(state_dim, action_dim)
        self.target_model = DQN(state_dim, action_dim)
        self.target_model.load_state_dict(self.model.state_dict())

        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        self.criterion = nn.MSELoss()

        self.memory = deque(maxlen=10_000)
        self.gamma = 0.99
        self.batch_size = 32

        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.05

    def act(self, state):
        # Selects an action using epsilon-greedy strategy.
        if random.random() < self.epsilon:
            return random.randint(0, 3)  # Explore
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.model(state_tensor)
            return torch.argmax(q_values).item()  # Exploit

    def store(self, transition):
        # Saves state, action, reward, and next_state tuple to memory.
        self.memory.append(transition)

    def train_step(self):
        # Performs one training step using a random minibatch from memory.
        if len(self.memory) < self.batch_size:
            return 0 

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states = zip(*batch)

        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards).unsqueeze(1)
        next_states = torch.FloatTensor(next_states)

        q_values = self.model(states).gather(1, actions)
        with torch.no_grad():
            max_next_q = self.target_model(next_states).max(1, keepdim=True)[0]
            target = rewards + self.gamma * max_next_q

        loss = self.criterion(q_values, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def update_target(self):
        # Synchronizes the target model with the main model.
        self.target_model.load_state_dict(self.model.state_dict())

    def decay_epsilon(self):
        # Gradually reduces epsilon value g to encourage more exploitation.
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

    def save(self, path="dqn_model.pt"):
        """Saves the model to a .pt file."""
        torch.save(self.model.state_dict(), path)

    def load(self, path="dqn_model.pt"):
        """Loads a model from a .pt file."""
        self.model.load_state_dict(torch.load(path))
        self.model.eval()
