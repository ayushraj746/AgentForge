from typing import Dict, Any


class Grader:
    def __init__(self):
        self.weights = {
            "correctness": 0.5,
            "completion": 0.2,
            "workflow": 0.15,
            "stability": 0.15,
        }

    def grade(self, state) -> Dict[str, Any]:
        scores = {}

        # -----------------------------
        # CORRECTNESS
        # -----------------------------
        if not state.test_results:
            correctness = 0.0
        elif state.test_results.get("passed"):
            correctness = 1.0
        else:
            correctness = state.test_results.get("score", 0.0)

        scores["correctness"] = correctness

        # -----------------------------
        # COMPLETION
        # -----------------------------
        if state.done:
            completion = 1.0
        else:
            completion = min(1.0, state.step_count / state.max_steps)

        scores["completion"] = completion

        # -----------------------------
        # WORKFLOW
        # -----------------------------
        tools_used = len(state.tool_usage)
        workflow = min(1.0, tools_used / 3)
        scores["workflow"] = workflow

        # -----------------------------
        # STABILITY
        # -----------------------------
        errors = len(state.errors)

        if errors == 0:
            stability = 1.0
        else:
            stability = max(0.0, 1 - (errors / 5))

        scores["stability"] = stability

        # -----------------------------
        # FINAL SCORE CALCULATION
        # -----------------------------
        final_score = sum(
            scores[k] * self.weights[k] for k in self.weights
        )

        # Debug logging
        print(f"[Grader Debug] Scores: {scores}")
        print(f"[Grader Debug] Final Score: {round(final_score, 4)}")

        return {
            "final_score": round(final_score, 4),
            "breakdown": scores,
            "success": final_score > 0.75
        }
