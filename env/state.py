from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class File(BaseModel):
    name: str
    content: str


class TestResult(BaseModel):
    passed: bool
    score: float
    errors: List[str] = Field(default_factory=list)


class EnvironmentState(BaseModel):
    # -----------------------------
    # CORE PROJECT STATE
    # -----------------------------
    files: Dict[str, str] = Field(default_factory=dict)
    current_task: str = ""
    task_metadata: Dict[str, Any] = Field(default_factory=dict)

    # -----------------------------
    # WORKFLOW / LIFECYCLE (🔥 NEW)
    # -----------------------------
    current_phase: str = "init"   # init → develop → test → debug → deploy
    completed_phases: List[str] = Field(default_factory=list)

    # -----------------------------
    # EXECUTION TRACKING
    # -----------------------------
    step_count: int = 0
    max_steps: int = 50
    done: bool = False

    # -----------------------------
    # SYSTEM ISSUES (🔥 UPGRADED)
    # -----------------------------
    errors: List[str] = Field(default_factory=list)
    active_issues: List[str] = Field(default_factory=list)

    # -----------------------------
    # TEST RESULTS
    # -----------------------------
    test_results: Dict[str, Any] = Field(default_factory=dict)

    # -----------------------------
    # INTELLIGENCE LAYER
    # -----------------------------
    history: List[Dict[str, Any]] = Field(default_factory=list)
    reasoning_trace: List[str] = Field(default_factory=list)

    # -----------------------------
    # AGENT BEHAVIOR TRACKING
    # -----------------------------
    tool_usage: Dict[str, int] = Field(default_factory=dict)
    retry_count: int = 0

    # -----------------------------
    # REWARD TRACKING
    # -----------------------------
    reward: float = 0.0
    cumulative_reward: float = 0.0

    # -----------------------------
    # EVENT SYSTEM (🔥 VERY IMPORTANT)
    # -----------------------------
    triggered_events: List[str] = Field(default_factory=list)

    # -----------------------------
    # TIMING
    # -----------------------------
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    # -----------------------------
    # UTILITY METHODS
    # -----------------------------

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    def start(self):
        self.start_time = datetime.utcnow().isoformat()

    def end(self):
        self.end_time = datetime.utcnow().isoformat()

    # -----------------------------
    # HISTORY + REASONING
    # -----------------------------
    def add_history(self, action: str, tool: str, result: Any, reward: float, reasoning: str):
        self.history.append({
            "step": self.step_count,
            "phase": self.current_phase,
            "action": action,
            "tool": tool,
            "result": result,
            "reward": reward,
            "reasoning": reasoning
        })

    def add_reasoning(self, text: str):
        self.reasoning_trace.append(text)

    # -----------------------------
    # TOOL TRACKING
    # -----------------------------
    def track_tool(self, tool_name: str):
        if tool_name not in self.tool_usage:
            self.tool_usage[tool_name] = 0
        self.tool_usage[tool_name] += 1

    # -----------------------------
    # STEP CONTROL
    # -----------------------------
    def increment_step(self):
        self.step_count += 1
        if self.step_count >= self.max_steps:
            self.done = True

    # -----------------------------
    # ERROR + ISSUE MANAGEMENT
    # -----------------------------
    def add_error(self, error: str):
        self.errors.append(error)
        self.active_issues.append(error)

    def resolve_issue(self, issue: str):
        if issue in self.active_issues:
            self.active_issues.remove(issue)

    # -----------------------------
    # REWARD
    # -----------------------------
    def update_reward(self, value: float):
        self.reward = value
        self.cumulative_reward += value

    # -----------------------------
    # RETRY LOGIC
    # -----------------------------
    def should_retry(self) -> bool:
        return self.retry_count < 3

    def increment_retry(self):
        self.retry_count += 1

    # -----------------------------
    # WORKFLOW CONTROL (🔥 IMPORTANT)
    # -----------------------------
    def set_phase(self, phase: str):
        if phase != self.current_phase:
            self.completed_phases.append(self.current_phase)
            self.current_phase = phase

    # -----------------------------
    # EVENT SYSTEM
    # -----------------------------
    def trigger_event(self, event: str):
        self.triggered_events.append(event)