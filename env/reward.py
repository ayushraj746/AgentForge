from typing import Dict, Any


class RewardCalculator:
    def __init__(self):
        # weights can be tuned
        self.weights = {
            "correctness": 0.5,
            "efficiency": 0.1,
            "tool_usage": 0.1,
            "progress": 0.2,
            "penalty": 0.1,
        }

    def compute(self, state, action: str, observation: Dict[str, Any]) -> float:
        reward = 0.0

        # -----------------------------
        # 1. CORRECTNESS (🔥 MOST IMPORTANT)
        # -----------------------------
        correctness_score = 0.0
        if "test_results" in observation:
            test_results = observation["test_results"]
            if test_results.get("passed"):
                correctness_score = 1.0
            else:
                correctness_score = test_results.get("score", 0.0)

        # -----------------------------
        # 2. EFFICIENCY (LESS STEPS = BETTER)
        # -----------------------------
        efficiency_score = max(
            0.0,
            1 - (state.step_count / state.max_steps)
        )

        # -----------------------------
        # 3. TOOL USAGE (SMART WORKFLOW)
        # -----------------------------
        tool_score = self._tool_usage_score(state)

        # -----------------------------
        # 4. PROGRESS (ISSUES RESOLVED)
        # -----------------------------
        progress_score = self._progress_score(state)

        # -----------------------------
        # 5. PENALTIES
        # -----------------------------
        penalty_score = self._penalty_score(state, action, observation)

        # -----------------------------
        # FINAL REWARD
        # -----------------------------
        reward = (
            self.weights["correctness"] * correctness_score
            + self.weights["efficiency"] * efficiency_score
            + self.weights["tool_usage"] * tool_score
            + self.weights["progress"] * progress_score
            - self.weights["penalty"] * penalty_score
        )

        return round(reward, 4)

    # -----------------------------
    # TOOL USAGE SCORE
    # -----------------------------
    def _tool_usage_score(self, state) -> float:
        if not state.tool_usage:
            return 0.0

        total_tools = len(state.tool_usage)

        # Encourage using multiple tools (not just code edit spam)
        return min(1.0, total_tools / 4)

    # -----------------------------
    # PROGRESS SCORE
    # -----------------------------
    def _progress_score(self, state) -> float:
        if not state.active_issues:
            return 1.0

        # fewer issues = better
        return max(0.0, 1 - (len(state.active_issues) / 5))

    # -----------------------------
    # PENALTY SYSTEM (🔥 IMPORTANT)
    # -----------------------------
    def _penalty_score(self, state, action: str, observation: Dict[str, Any]) -> float:
        penalty = 0.0

        # Too many retries
        if state.retry_count > 2:
            penalty += 0.2

        # Error in observation
        if "error" in str(observation).lower():
            penalty += 0.2

        # Spamming same action
        if len(state.history) >= 2:
            if state.history[-1]["action"] == action:
                penalty += 0.1

        # No tool usage (bad workflow)
        if not state.tool_usage:
            penalty += 0.2

        return penalty