from typing import Dict, List, Any
from pydantic import BaseModel, Field


class File(BaseModel):
    name: str
    content: str


class TestResult(BaseModel):
    passed: bool
    score: float
    errors: List[str] = Field(default_factory=list)


class EnvironmentState(BaseModel):
    # Files in project
    files: Dict[str, str] = Field(default_factory=dict)

    # Current task description
    current_task: str = ""

    # Step counter
    step_count: int = 0
    max_steps: int = 50

    # Errors in system
    errors: List[str] = Field(default_factory=list)

    # Test results
    test_results: Dict[str, Any] = Field(default_factory=dict)

    # History of actions
    history: List[Dict[str, Any]] = Field(default_factory=list)

    # Completion flag
    done: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    def add_history(self, action: str, result: Any):
        self.history.append({
            "step": self.step_count,
            "action": action,
            "result": result
        })

    def increment_step(self):
        self.step_count += 1
        if self.step_count >= self.max_steps:
            self.done = True