# Purpose: Train the DQN agent using simulated bug report data and log rewards to a file.

# Requirements:
# ```bash
# pip install torchvision
#
# ``bash
# pip3 install torchvision
#
# Alternatively, installation can be done through homebrew:
# ```bash
# brew install pipx

from models.rl_agent.rl_env import BugBountyEnv
from models.rl_agent.dqn_agent import DQNAgent
import numpy as np
import time
import json
from pathlib import Path

# Configuration
EPISODES = 1000
SAVE_EVERY = 100
LOG_PATH = Path("logs/training_rewards.json")

env = BugBountyEnv()
agent = DQNAgent(state_dim=2, action_dim=4)
rewards_log = []

for ep in range(1, EPISODES + 1):
    state = env.reset()
    action = agent.act(state)
    next_state, reward, done, _ = env.step(action)
    agent.store((state, action, reward, next_state))
    loss = agent.train_step()
    agent.decay_epsilon()

    rewards_log.append(reward)

    if ep % SAVE_EVERY == 0:
        agent.update_target()
        agent.save()
        LOG_PATH.parent.mkdir(exist_ok=True)
        LOG_PATH.write_text(json.dumps(rewards_log))
        print(f"[{ep}] Reward: {reward:.2f} | Epsilon: {agent.epsilon:.3f}")

print("Training complete.")
