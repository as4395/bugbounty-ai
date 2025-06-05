import random

class BugBountyEnvironment:
    def __init__(self):
        self.state = {
            'programs_scraped': 0,
            'vulns_found': 0,
            'reports_submitted': 0
        }
        self.valid_actions = ['scan', 'report', 'submit']

    def reset(self):
        self.state = {
            'programs_scraped': 0,
            'vulns_found': 0,
            'reports_submitted': 0
        }
        print("[Env] Environment reset.")
        return self.state

    def get_valid_actions(self):
        return self.valid_actions

    def step(self, action):
        reward = self.simulate_reward(action)

        # Update state
        if action == 'scan':
            self.state['programs_scraped'] += 1
        elif action == 'report':
            self.state['vulns_found'] += 1
        elif action == 'submit':
            self.state['reports_submitted'] += 1

        # Example condition (when 5 reports submitted)
        done = self.state['reports_submitted'] >= 5

        print(f"[Env] Action '{action}' → Reward: {reward}, State: {self.state}")
        return self.state, reward, done

    def simulate_reward(self, action):
        if action == 'scan':
            return random.choice([1, 2])
        elif action == 'report':
            return random.choice([2, 3])
        elif action == 'submit':
            return random.choice([3, 5])
        return 0
