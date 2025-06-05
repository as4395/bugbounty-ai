import random
import json

class BugBountyAgent:
    def __init__(self, actions):
        self.actions = actions
        self.q_table = {action: 0 for action in actions}

    def choose_action(self):
        # Randomly select one of the available actions
        action = random.choice(self.actions)
        print(f"[Agent] Chose action: {action}")
        return action

    def update(self, action, reward):
        # Increase score for the selected action
        print(f"[Agent] Updating '{action}' with reward {reward}")
        self.q_table[action] += reward

    def save(self, filepath):
        # Save the Q-table to a file in JSON format
        with open(filepath, 'w') as f:
            json.dump(self.q_table, f)
        print(f"[Agent] Q-table saved to {filepath}")

    def load(self, filepath):
        # Load the Q-table from a JSON file
        with open(filepath, 'r') as f:
            self.q_table = json.load(f)
        print(f"[Agent] Q-table loaded from {filepath}")
