from typing import Dict, Any

from env.state import EnvironmentState
from tools.code_editor import CodeEditor
from tools.test_runner import TestRunner
from tools.doc_search import DocSearchTool
from tools.git import GitTool
from tools.terminal import TerminalTool

from env.tasks import TaskManager
from env.reward import RewardCalculator
from env.grader import Grader


class AgentForgeEnv:
    def __init__(self):
        self.state = EnvironmentState()

        # Tools
        self.test_runner = TestRunner()
        self.doc_search = DocSearchTool()
        self.git = GitTool()
        self.terminal = TerminalTool()

        # Core systems
        self.task_manager = TaskManager()
        self.reward_calculator = RewardCalculator()
        self.grader = Grader()

        # Event system
        self.events = [
            {"step": 3, "type": "requirement_change"},
            {"step": 5, "type": "performance_issue"},
            {"step": 7, "type": "dependency_break"}
        ]

    # ---------------- RESET ---------------- #
    def reset(self, task: str = "easy") -> Dict[str, Any]:
        self.state = EnvironmentState()

        task_data = self.task_manager.get_task(task)

        self.state.files = task_data["files"].copy()
        self.state.current_task = task_data["description"]
        self.state.task_metadata = task_data

        self.state.start()

        return self.state.to_dict()

    # ---------------- STEP ---------------- #
    def step(self, action: Dict[str, Any]) -> Dict[str, Any]:
        if self.state.done:
            return {
                "error": "Episode already finished",
                "state": self.state.to_dict(),
                "done": True,
                "reward": 0.0
            }

        tool = action.get("tool")
        params = action.get("params", {})
        reasoning = action.get("reasoning", "No reasoning provided")

        result = None

        # Track reasoning
        self.state.add_reasoning(reasoning)

        # Initialize editor
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

            elif tool == "doc_search":
                result = self.doc_search.search(**params)

            elif tool == "git_commit":
                result = self.git.commit(self.state, **params)

            elif tool == "git_log":
                result = self.git.log()

            elif tool == "terminal":
                result = self.terminal.run(self.state, **params)

            else:
                result = f"Unknown tool: {tool}"
                self.state.add_error(result)

            # Track tool usage
            self.state.track_tool(tool)

        except Exception as e:
            result = f"Error executing tool: {str(e)}"
            self.state.add_error(result)

        # -------- APPLY EVENTS (🔥 IMPORTANT) -------- #
        self._apply_events()

        # -------- STEP UPDATE -------- #
        self.state.increment_step()

        # -------- REWARD -------- #
        reward = self.reward_calculator.compute(
            self.state,
            action=str(action),
            observation={"test_results": self.state.test_results, "result": result}
        )
        self.state.update_reward(reward)

        # -------- HISTORY -------- #
        self.state.add_history(
            action=str(action),
            tool=tool,
            result=result,
            reward=reward,
            reasoning=reasoning
        )

        # -------- DONE CONDITION -------- #
        if self.state.test_results.get("passed"):
            self.state.done = True

        if self.state.step_count >= self.state.max_steps:
            self.state.done = True

        if self.state.done:
            self.state.end()

        return {
            "state": self.state.to_dict(),
            "reward": reward,
            "done": self.state.done,
            "result": result
        }

    # ---------------- EVENTS SYSTEM ---------------- #
    def _apply_events(self):
        for event in self.events:
            if self.state.step_count == event["step"]:
                self._trigger_event(event["type"])

    def _trigger_event(self, event_type: str):
        if event_type == "requirement_change":
            self.state.current_task += " | NEW: handle edge cases"
            self.state.trigger_event(event_type)

        elif event_type == "performance_issue":
            self.state.add_error("Performance degradation detected")
            self.state.trigger_event(event_type)

        elif event_type == "dependency_break":
            self.state.add_error("Dependency conflict in utils.py")
            self.state.trigger_event(event_type)

    # ---------------- FINAL EVALUATION ---------------- #
    def evaluate(self) -> Dict[str, Any]:
        return self.grader.grade(self.state)

    # ---------------- STATE ---------------- #
    def get_state(self) -> Dict[str, Any]:
        return self.state.to_dict()