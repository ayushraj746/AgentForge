from typing import Dict, Any


class TaskManager:
    def __init__(self):
        self.tasks = {
            "easy": self._easy_task(),
            "medium": self._medium_task(),
            "hard": self._hard_task(),
            "hard_plus": self._hard_plus_task()  # optional bonus
        }

    def get_task(self, difficulty: str) -> Dict[str, Any]:
        return self.tasks.get(difficulty, self._easy_task())

    # ---------------- EASY ---------------- #
    def _easy_task(self) -> Dict[str, Any]:
        return {
            "id": "easy_sum_fix",
            "difficulty": "easy",
            "description": "Fix the function to return correct sum of two numbers.",
            "files": {
                "main.py": """
def add(a, b):
    # BUG: incorrect implementation
    return a - b
"""
            },
            "goal": "Function should correctly return sum of a and b",
            "expected_behavior": "add(2,3) == 5",
            "hints": [
                "Check arithmetic operation",
                "Use correct operator for addition"
            ]
        }

    # ---------------- MEDIUM ---------------- #
    def _medium_task(self) -> Dict[str, Any]:
        return {
            "id": "medium_list_processing",
            "difficulty": "medium",
            "description": "Refactor code to handle list of numbers and return their sum with validation.",
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
            "goal": "Handle edge cases like empty list, invalid input, and ensure correct sum",
            "expected_behavior": "sum_list([1,2,3]) == 6",
            "hints": [
                "Check for empty input",
                "Validate input properly"
            ]
        }

    # ---------------- HARD ---------------- #
    def _hard_task(self) -> Dict[str, Any]:
        return {
            "id": "hard_dynamic_processing",
            "difficulty": "hard",
            "description": "Implement optimized function with changing requirements and performance constraints.",
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
            "goal": "Implement processing, adapt to requirement changes, and optimize performance",
            "expected_behavior": "Function adapts to config REQUIREMENT dynamically",
            "hints": [
                "Read config dynamically",
                "Support multiple behaviors",
                "Optimize loops"
            ]
        }

    # ---------------- HARD PLUS (OPTIONAL BONUS) ---------------- #
    def _hard_plus_task(self) -> Dict[str, Any]:
        return {
            "id": "hard_plus_adaptive_system",
            "difficulty": "hard",
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
            "goal": "Implement dynamic processing, support multiple modes, and handle edge cases robustly",
            "expected_behavior": "Supports sum and average modes correctly",
            "hints": [
                "Handle multiple modes",
                "Add error handling",
                "Ensure robustness"
            ]
        }