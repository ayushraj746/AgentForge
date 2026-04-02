from typing import Dict, Any


class TestRunner:
    def __init__(self):
        pass

    def run_tests(self, files: Dict[str, str]) -> Dict[str, Any]:
        """
        Simulated test runner.
        Checks for basic correctness patterns.
        """

        result = {
            "passed": False,
            "score": 0.0,
            "errors": []
        }

        # Simple rule-based checks
        if "main.py" not in files:
            result["errors"].append("main.py missing")
            return result

        code = files["main.py"]

        # Check for basic function existence
        if "def" not in code:
            result["errors"].append("No function defined")
        else:
            result["score"] += 0.4

        # Check for return statement
        if "return" not in code:
            result["errors"].append("Missing return statement")
        else:
            result["score"] += 0.3

        # Check for logic keywords
        if "if" in code or "for" in code:
            result["score"] += 0.3

        # Final pass condition
        if result["score"] >= 0.7:
            result["passed"] = True

        return result