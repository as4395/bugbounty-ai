import random

def epsilon_greedy(q_table, actions, epsilon=0.2):
    """
    Select an action using the epsilon-greedy strategy:
    - With probability ε, explore by picking a random action.
    - Otherwise, exploit the best-known action from the Q-table.
    """
    if not q_table or random.random() < epsilon:
        return random.choice(actions)

    # Pick the action with the highest Q-value
    return max(q_table, key=q_table.get)

def normalize_q_table(q_table):
    """
    Normalize Q-values in the table to a 0–1 range.
    This helps with visualization or monitoring learning progress.
    """
    if not q_table:
        return {}

    values = list(q_table.values())
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val or 1  # avoid division by zero

    normalized = {
        action: round((val - min_val) / range_val, 3)
        for action, val in q_table.items()
    }

    return normalized
