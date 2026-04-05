from typing import Dict, Any


class TaskManager:
    def __init__(self):
        self.tasks = {
            "easy": self._easy_task(),
            "medium": self._medium_task(),
            "hard": self._hard_task(),
            "hard_plus": self._hard_plus_task()
        }

    def get_task(self, difficulty: str) -> Dict[str, Any]:
        return self.tasks.get(difficulty, self._easy_task())

    # ---------------- EASY ---------------- #
    def _easy_task(self) -> Dict[str, Any]:
        return {
            "description": "Fix the function to return correct sum of two numbers.",
            "files": {
                "main.py": """
def add(a, b):
    # BUG: incorrect implementation
    return a - b
"""
            },
            "goal": "Function should correctly return sum of a and b"
        }

    # ---------------- MEDIUM ---------------- #
    def _medium_task(self) -> Dict[str, Any]:
        return {
            "description": "Refactor code to handle list of numbers and return their sum.",
            "files": {
                "main.py": """
def sum_list(numbers):
    total = 0
    for n in numbers:
        total += n
    return total
""",
                "utils.py": """
# BUG: missing edge case handling
def validate(numbers):
    return isinstance(numbers, list)
"""
            },
            "goal": "Handle edge cases and ensure correct sum"
        }

    # ---------------- HARD ---------------- #
    def _hard_task(self) -> Dict[str, Any]:
        return {
            "description": "Implement optimized function with changing requirements.",
            "files": {
                "main.py": """
def process_data(data):
    # TODO: implement processing
    return None
""",
                "config.py": """
REQUIREMENT = "sum"
"""
            },
            "goal": "Implement processing, adapt to requirement changes, and optimize performance"
        }

    # ---------------- HARD PLUS ---------------- #
    def _hard_plus_task(self) -> Dict[str, Any]:
        return {
            "description": "Handle dynamic requirements and implement adaptive processing with error handling.",
            "files": {
                "main.py": """
def process_data(data, mode="sum"):
    # TODO: implement dynamic processing based on mode
    # modes: sum, average
    return None
""",
                "config.py": """
REQUIREMENT = "dynamic"
"""
            },
            "goal": "Implement dynamic processing, support multiple modes, and handle edge cases robustly"
        }