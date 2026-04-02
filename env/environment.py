from typing import Dict, Any

from env.state import EnvironmentState
from tools.code_editor import CodeEditor
from tools.test_runner import TestRunner


class AgentForgeEnv:
    def __init__(self):
        self.state = EnvironmentState()
        self.test_runner = TestRunner()

    # ---------------- RESET ---------------- #
    def reset(self, task: str = "easy") -> Dict[str, Any]:
        """
        Initialize environment with a task
        """
        self.state = EnvironmentState()

        # Basic starter file
        self.state.files = {
            "main.py": "# TODO: implement function\n"
        }

        self.state.current_task = task
        self.state.step_count = 0
        self.state.done = False
        self.state.errors = []
        self.state.test_results = {}

        return self.state.to_dict()

    # ---------------- STEP ---------------- #
    def step(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute one action
        """
        if self.state.done:
            return {
                "error": "Episode already finished"
            }

        tool = action.get("tool")
        params = action.get("params", {})

        result = None

        # Initialize tools with current state
        editor = CodeEditor(self.state.files)

        # -------- TOOL EXECUTION -------- #
        if tool == "create_file":
            result = editor.create_file(**params)

        elif tool == "edit_file":
            result = editor.edit_file(**params)

        elif tool == "append_file":
            result = editor.append_to_file(**params)

        elif tool == "delete_file":
            result = editor.delete_file(**params)

        elif tool == "run_tests":
            result = self.test_runner.run_tests(self.state.files)
            self.state.test_results = result

        else:
            result = f"Unknown tool: {tool}"

        # -------- UPDATE STATE -------- #
        self.state.increment_step()
        self.state.add_history(str(action), result)

        # -------- REWARD -------- #
        reward = self._calculate_reward()

        # -------- DONE CONDITION -------- #
        if self.state.test_results.get("passed"):
            self.state.done = True

        return {
            "state": self.state.to_dict(),
            "reward": reward,
            "done": self.state.done,
            "result": result
        }

    # ---------------- STATE ---------------- #
    def get_state(self) -> Dict[str, Any]:
        return self.state.to_dict()

    # ---------------- REWARD ---------------- #
    def _calculate_reward(self) -> float:
        """
        Simple reward function
        """
        reward = 0.0

        # Reward for passing tests
        if self.state.test_results.get("passed"):
            reward += 1.0

        # Partial score
        reward += self.state.test_results.get("score", 0.0)

        # Penalty for too many steps
        reward -= 0.01 * self.state.step_count

        return max(reward, 0.0)