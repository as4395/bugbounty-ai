# Purpose: 
#   Use the trained RL agent to recommend which platform a bug report should be submitted to.

from models.rl_agent.dqn_agent import DQNAgent
from models.rl_agent.rl_env import BugBountyEnv

# Usage:
# Train the model first using:
#   python scripts/train_rl_agent.py
#
# Then run:
#   python scripts/submitter.py

# Load environment and agent
env = BugBountyEnv()
agent = DQNAgent(state_dim=2, action_dim=4)
agent.load("dqn_model.pt")

# Simulate new bug report
state = env.reset()
action = agent.act(state)

# Map action index to a human-readable decision
platform_map = {
    0: "Skip submission",
    1: "HackerOne",
    2: "Bugcrowd",
    3: "Intigriti"
}

# Decode and display report details
type_idx, sev_idx = int(state[0]), int(state[1])
print(f"\n New Bug Report:")
print(f"  * Type: {env.report_types[type_idx]}")
print(f"  * Severity: {env.severities[sev_idx]}")
print(f"\n Agent recommends: {platform_map[action]}")
