from typing import Dict, Any


class TestRunner:
    def __init__(self):
        pass

    def run_tests(self, files: Dict[str, str]) -> Dict[str, Any]:
        """
        Smarter test runner that checks actual logic patterns.
        """

        result = {
            "passed": False,
            "score": 0.0,
            "errors": []
        }

        if "main.py" not in files:
            result["errors"].append("main.py missing")
            return result

        code = files["main.py"]

        # -----------------------------
        # BASIC STRUCTURE CHECKS
        # -----------------------------
        if "def" not in code:
            result["errors"].append("No function defined")
            return result
        else:
            result["score"] += 0.2

        if "return" not in code:
            result["errors"].append("Missing return statement")
            return result
        else:
            result["score"] += 0.2

        # -----------------------------
        # LOGIC CHECKS (🔥 IMPORTANT)
        # -----------------------------

        # Case 1: ADD FUNCTION
        if "add" in code:
            if "return a + b" in code:
                result["score"] += 0.6
            else:
                result["errors"].append("Incorrect addition logic (should be a + b)")

        # Case 2: SUM LIST
        elif "sum_list" in code:
            if "sum(" in code or "for" in code:
                result["score"] += 0.6
            else:
                result["errors"].append("List summation logic incorrect")

        # Case 3: DIVIDE FUNCTION
        elif "divide" in code:
            if "if b != 0" in code:
                result["score"] += 0.6
            else:
                result["errors"].append("Division by zero not handled")

        # Case 4: GENERIC PROCESSING
        elif "process_data" in code:
            if "sum(" in code or "max(" in code:
                result["score"] += 0.6
            else:
                result["errors"].append("Processing logic incomplete")

        # -----------------------------
        # FINAL DECISION
        # -----------------------------
        if result["score"] >= 0.8:
            result["passed"] = True

        return result