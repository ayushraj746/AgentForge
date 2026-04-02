import os
import json


class HybridAgent:
    def __init__(self):
        self.use_openai = bool(os.getenv("OPENAI_API_KEY"))

    def decide_action(self, state):
        if self.use_openai:
            try:
                action = self._llm_decision(state)

                # safety check
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

        # -------- SAFE PARSING -------- #
        try:
            # remove markdown if present
            if content.startswith("```"):
                content = content.split("```")[1]

            action = json.loads(content)
            return action

        except Exception:
            return self._rule_based(state)