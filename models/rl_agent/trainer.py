from agent import BugBountyAgent
from env import BugBountyEnvironment
import time

def train(episodes=10):
    env = BugBountyEnvironment()
    agent = BugBountyAgent(actions=env.get_valid_actions())

    for ep in range(episodes):
        print(f"\n--- Episode {ep + 1} ---")
        state = env.reset()

        for step in range(20):  # Limit steps per episode
            action = agent.choose_action()
            next_state, reward, done = env.step(action)
            agent.update(action, reward)

            if done:
                print("[Trainer] Episode finished early.")
                break

            time.sleep(0.2)  # Small delay for readability

    agent.save("models/rl_agent/q_table.json")
    print("\n[Trainer] Training complete.")

if __name__ == "__main__":
    train()
