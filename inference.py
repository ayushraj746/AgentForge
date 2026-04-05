import os
import json
import time

from env.environment import AgentForgeEnv

print("🚀 File running")


# ---------------- AGENT ---------------- #
class HybridAgent:
    def __init__(self):
        self.use_openai = bool(os.getenv("OPENAI_API_KEY"))
        print(f"[Agent] OpenAI Enabled: {self.use_openai}")  # 🔥 logging

    def decide_action(self, state):
        print("[Agent] Deciding action...")  # 🔥 logging

        if self.use_openai:
            try:
                action = self._llm_decision(state)

                if isinstance(action, dict) and "tool" in action:
                    action["reasoning"] = "LLM-based decision"
                    return action

            except Exception as e:
                print("[Agent] LLM failed, using fallback:", e)

        return self._rule_based(state)

    # ---------------- FAILURE ANALYSIS ---------------- #
    def _analyze_failure(self, test_results):
        errors = test_results.get("errors", [])

        if not errors:
            return "No clear error found"

        error = errors[0].lower()

        if "addition" in error:
            return "Function is using subtraction instead of addition"

        if "processing logic incomplete" in error:
            return "Processing logic missing, should aggregate data"

        if "division" in error:
            return "Division not handling edge cases like divide by zero"

        return "General logic issue detected"

    # ---------------- RULE-BASED AGENT ---------------- #
    def _rule_based(self, state):
        files = state.get("files", {})
        test_results = state.get("test_results", {})
        step = state.get("step_count", 0)
        tool_usage = state.get("tool_usage", {})

        # PHASE 1: UNDERSTAND
        if step == 0:
            return {
                "tool": "doc_search",
                "params": {"query": state.get("current_task", "")},
                "reasoning": "Understanding task via documentation"
            }

        # PHASE 2: TEST
        if not test_results:
            return {
                "tool": "run_tests",
                "params": {},
                "reasoning": "Running tests to detect failures"
            }

        # PHASE 3: DEBUG
        if not test_results.get("passed"):

            diagnosis = self._analyze_failure(test_results)
            print("[Agent] Diagnosis:", diagnosis)

            if "main.py" in files:
                code = files["main.py"]

                if (
                    "return a + b" in code
                    or "return sum(" in code
                    or "if b != 0" in code
                ):
                    return {
                        "tool": "run_tests",
                        "params": {},
                        "reasoning": f"Verifying fix ({diagnosis})"
                    }

            if "doc_search" not in tool_usage:
                return {
                    "tool": "doc_search",
                    "params": {"query": str(test_results)},
                    "reasoning": f"Searching solution ({diagnosis})"
                }

            if "main.py" in files:
                code = files["main.py"]

                if "return a - b" in code:
                    new_code = code.replace("return a - b", "return a + b")

                elif "return None" in code:
                    new_code = code.replace("return None", "return sum(data)")

                elif "return a / b" in code:
                    new_code = code.replace(
                        "return a / b",
                        "return a / b if b != 0 else 0"
                    )

                else:
                    new_code = code + "\n# fallback fix applied"

                return {
                    "tool": "edit_file",
                    "params": {
                        "filename": "main.py",
                        "new_content": new_code
                    },
                    "reasoning": f"Fixing code ({diagnosis})"
                }

        # PHASE 4: VALIDATE
        if not test_results.get("passed"):
            return {
                "tool": "run_tests",
                "params": {},
                "reasoning": "Re-running tests after fix"
            }

        # PHASE 5: COMMIT
        if "git_commit" not in tool_usage:
            return {
                "tool": "git_commit",
                "params": {"message": "Fix applied and validated"},
                "reasoning": "Saving stable version"
            }

        # PHASE 6: TERMINAL
        if "terminal" not in tool_usage:
            return {
                "tool": "terminal",
                "params": {"command": "ls"},
                "reasoning": "Inspecting project structure"
            }

        return {
            "tool": "run_tests",
            "params": {},
            "reasoning": "Final verification"
        }

    # ---------------- LLM ---------------- #
    def _llm_decision(self, state):
        from openai import OpenAI

        client = OpenAI()

        prompt = f"""
You are an autonomous software engineering agent.

State:
{state}

Return ONLY JSON:
{{"tool": "...", "params": {{...}}}}
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
            print("[Agent] LLM parsing failed, fallback triggered")
            return self._rule_based(state)


# ---------------- RUN EPISODE ---------------- #
def run_episode(task="easy", max_steps=20):
    env = AgentForgeEnv()
    agent = HybridAgent()

    state = env.reset(task=task)

    print(f"\n🚀 Task: {task}")
    print(f"📝 {state['current_task']}")

    total_reward = 0.0

    for step in range(max_steps):
        print(f"\n--- Step {step+1} ---")

        action = agent.decide_action(state)
        print("🧠 Reasoning:", action.get("reasoning"))
        print("⚡ Action:", action)

        result = env.step(action)

        state = result["state"]
        reward = result["reward"]
        done = result["done"]

        total_reward += reward

        print("📌 Result:", result["result"])
        print("💰 Reward:", reward)

        if done:
            print("\n✅ Task Completed!")
            break

        time.sleep(0.2)

    evaluation = env.evaluate()

    print("\n📊 Final Reward:", total_reward)
    print("📊 Evaluation:", evaluation)

    return total_reward


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    print("\n🔥 Starting AgentForge System...\n")

    for task in ["easy", "medium", "hard", "hard_plus"]:
        print("\n" + "=" * 50)
        run_episode(task)