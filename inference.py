import os
import random

# --- Import your env + policy ---
# Make sure these imports match your file structure later
from environment import EmailTriageEnvironment
from policies import RuleBasedEmailPolicy

def run_episode(env, policy):
    obs = env.reset()

    print("[START]")
    print(f"email: {obs.email_text}")
    print(f"stage: {obs.current_stage}")

    total_reward = 0

    while not obs.done:
        action = policy.select_action(obs)

        print("[STEP]")
        print(f"stage: {obs.current_stage}")
        print(f"action: {action.content}")

        obs = env.step(action)

        print(f"reward: {obs.reward}")
        print(f"next_stage: {obs.current_stage}")
        print(f"message: {obs.message}")

        if obs.reward is not None:
            total_reward += obs.reward

    print("[END]")
    print(f"final_score: {total_reward}")
    print(f"steps: {env.state.step_count}")

    return total_reward


def main():
    # Required env variables (from checklist)
    API_BASE_URL = os.getenv("API_BASE_URL")
    MODEL_NAME = os.getenv("MODEL_NAME")
    HF_TOKEN = os.getenv("HF_TOKEN")

    env = EmailTriageEnvironment()
    policy = RuleBasedEmailPolicy()

    episodes = 10
    scores = []

    for _ in range(episodes):
        score = run_episode(env, policy)
        scores.append(score)

    avg_score = sum(scores) / len(scores)

    print("\n[SUMMARY]")
    print(f"episodes: {episodes}")
    print(f"average_score: {avg_score}")


if __name__ == "__main__":
    main()
