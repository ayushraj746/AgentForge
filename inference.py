import os
import json
import time

from env.environment import AgentForgeEnv

print("🚀 File running")


# ---------------- AGENT ---------------- #
class HybridAgent:
    def __init__(self):
        self.use_openai = bool(os.getenv("OPENAI_API_KEY"))

    def decide_action(self, state):
        if self.use_openai:
            try:
                action = self._llm_decision(state)

                if isinstance(action, dict) and "tool" in action:
                    return action

            except Exception as e:
                print("LLM failed, using fallback:", e)

        return self._rule_based(state)

    def _rule_based(self, state):
        files = state.get("files", {})
        test_results = state.get("test_results", {})

        # 1. Run tests first
        if not test_results:
            return {"tool": "run_tests", "params": {}}

        # 2. Fix code if failing
        if not test_results.get("passed"):
            if "main.py" in files:
                code = files["main.py"]

                if "return a - b" in code:
                    new_code = code.replace("return a - b", "return a + b")
                elif "return None" in code:
                    new_code = code.replace("return None", "return sum(data)")
                else:
                    new_code = code + "\n# fallback fix applied"

                return {
                    "tool": "edit_file",
                    "params": {
                        "filename": "main.py",
                        "new_content": new_code
                    }
                }

        # 3. Re-run tests
        return {"tool": "run_tests", "params": {}}

    def _llm_decision(self, state):
        from openai import OpenAI

        client = OpenAI()

        prompt = f"""
You are an AI coding agent.

Current state:
{state}

Return ONLY valid JSON like:
{{"tool": "edit_file", "params": {{"filename": "main.py", "new_content": "..."}}}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content.strip()

        try:
            if content.startswith("```"):
                content = content.split("```")[1]

            return json.loads(content)

        except Exception:
            return self._rule_based(state)


# ---------------- RUN EPISODE ---------------- #
def run_episode(task="easy", max_steps=20):
    env = AgentForgeEnv()
    agent = HybridAgent()

    state = env.reset(task=task)

    print(f"\n🚀 Starting Task: {task}")
    print(f"📝 Description: {state['current_task']}")

    total_reward = 0.0

    for step in range(max_steps):
        print(f"\n--- Step {step+1} ---")

        action = agent.decide_action(state)
        print("Action:", action)

        result = env.step(action)

        state = result["state"]
        reward = result["reward"]
        done = result["done"]

        total_reward += reward

        print("Result:", result["result"])
        print("Reward:", reward)

        if done:
            print("\n✅ Task Completed!")
            break

        time.sleep(0.3)

    print("\n📊 Final Score:", total_reward)
    print("Steps Taken:", state["step_count"])

    return total_reward


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    print("\n🔥 Starting AgentForge System...\n")

    for task in ["easy", "medium", "hard"]:
        print("\n" + "=" * 50)
        run_episode(task)