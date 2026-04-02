from typing import Dict, Any

from env.state import EnvironmentState
from tools.code_editor import CodeEditor
from tools.test_runner import TestRunner
from env.tasks import TaskManager


class AgentForgeEnv:
    def __init__(self):
        self.state = EnvironmentState()
        self.test_runner = TestRunner()
        self.task_manager = TaskManager()

    # ---------------- RESET ---------------- #
    def reset(self, task: str = "easy") -> Dict[str, Any]:
        """
        Initialize environment with a selected task
        """
        self.state = EnvironmentState()

        # Load task
        task_data = self.task_manager.get_task(task)

        self.state.files = task_data["files"].copy()
        self.state.current_task = task_data["description"]

        self.state.step_count = 0
        self.state.done = False
        self.state.errors = []
        self.state.test_results = {}

        return self.state.to_dict()

    # ---------------- STEP ---------------- #
    def step(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute one action in the environment
        """
        if self.state.done:
            return {
                "error": "Episode already finished",
                "state": self.state.to_dict(),
                "done": True,
                "reward": 0.0
            }

        tool = action.get("tool")
        params = action.get("params", {})

        result = None

        # Initialize tools with current state
        editor = CodeEditor(self.state.files)

        try:
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
                self.state.errors.append(result)

        except Exception as e:
            result = f"Error executing tool: {str(e)}"
            self.state.errors.append(result)

        # -------- UPDATE STATE -------- #
        self.state.increment_step()
        self.state.add_history(str(action), result)

        # -------- REWARD -------- #
        reward = self._calculate_reward()

        # -------- DONE CONDITION -------- #
        if self.state.test_results.get("passed"):
            self.state.done = True

        # Also stop if max steps reached
        if self.state.step_count >= self.state.max_steps:
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
        Advanced reward function (judge-level)
        """
        reward = 0.0

        test_result = self.state.test_results

        # 1. Partial correctness reward
        reward += test_result.get("score", 0.0)

        # 2. Full completion bonus
        if test_result.get("passed"):
            reward += 1.0

        # 3. Penalty for errors
        reward -= 0.05 * len(self.state.errors)

        # 4. Efficiency bonus (fewer steps = better)
        reward += max(0, 0.5 - 0.01 * self.state.step_count)

        # 5. Penalty if no tests run yet
        if not test_result:
            reward -= 0.1

        return max(reward, 0.0)