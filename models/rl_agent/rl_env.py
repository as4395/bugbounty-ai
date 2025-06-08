# Purpose: Simulate a simplified bug bounty environment for training a reinforcement learning agent.
# Each report has a type and severity. Actions determine where to submit or skip, and rewards are based on severity and simulated platform responses.

import numpy as np
import random

class BugBountyEnv:
    """
    Simulated environment for bug report handling.

    State = [report_type, severity].
    Actions:
        0 → Skip submission
        1 → Submit to HackerOne
        2 → Submit to Bugcrowd
        3 → Submit to Intigriti
    """

    def __init__(self):
        # Define report types and severities
        self.report_types = ['xss', 'sqli', 'rce']
        self.severities = ['low', 'medium', 'high']
        self.state = None

    def reset(self):
        # Start a new episode by generating a fresh report.
        self.state = self._generate_report()
        return self._encode_state(self.state)

    def step(self, action):
        """
        Simulate one interaction: the agent takes an action, receives a reward, and is given a new state. 
        This environment runs one step per episode.
        """
        reward = self._simulate_reward(self.state, action)
        done = True  # Each report is one-shot
        self.state = self._generate_report()
        next_state = self._encode_state(self.state)
        return next_state, reward, done, {}

    def _generate_report(self):
        # Randomly create a simulated bug report.
        return {
            'type': random.choice(self.report_types),
            'severity': random.choice(self.severities)
        }

    def _encode_state(self, report):
        """
        Convert a report into a 2D numeric state vector:
        [index of report type, index of severity]
        """
        type_index = self.report_types.index(report['type'])
        severity_index = self.severities.index(report['severity'])
        return np.array([type_index, severity_index], dtype=np.float32)

    def _simulate_reward(self, report, action):
        # Determine the reward based on the severity of the report and the action taken.
        if action == 0:
            return 0  # Skip = neutral

        base_reward = {
            'low': 2,
            'medium': 5,
            'high': 10
        }[report['severity']]

        # Add noise to simulate platform acceptance randomness
        reward_noise = random.choice([-1, 0, 1])
        return base_reward + reward_noise
