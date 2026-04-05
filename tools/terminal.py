from typing import Dict, Any


class TerminalTool:
    def __init__(self):
        self.history = []

    # -----------------------------
    # EXECUTE COMMAND
    # -----------------------------
    def run(self, state, command: str) -> Dict[str, Any]:
        command = command.strip()
        self.history.append(command)

        # -----------------------------
        # LIST FILES
        # -----------------------------
        if command == "ls":
            return {
                "status": "success",
                "output": list(state.files.keys())
            }

        # -----------------------------
        # READ FILE
        # -----------------------------
        if command.startswith("cat "):
            filename = command.split(" ", 1)[1]

            if filename in state.files:
                return {
                    "status": "success",
                    "output": state.files[filename]
                }
            else:
                return {
                    "status": "error",
                    "output": f"File '{filename}' not found"
                }

        # -----------------------------
        # PRINT TEXT
        # -----------------------------
        if command.startswith("echo "):
            return {
                "status": "success",
                "output": command.replace("echo ", "")
            }

        # -----------------------------
        # SIMULATE PYTHON EXECUTION
        # -----------------------------
        if command.startswith("python "):
            filename = command.split(" ", 1)[1]

            if filename in state.files:
                content = state.files[filename]

                # simple simulation
                if "return None" in content:
                    return {
                        "status": "error",
                        "output": "Program returned None (likely incomplete implementation)"
                    }

                return {
                    "status": "success",
                    "output": "Program executed successfully"
                }
            else:
                return {
                    "status": "error",
                    "output": f"File '{filename}' not found"
                }

        # -----------------------------
        # RUN TESTS (SIMULATED TRIGGER)
        # -----------------------------
        if command == "run tests":
            return {
                "status": "info",
                "output": "Use test_runner tool to execute tests"
            }

        # -----------------------------
        # UNKNOWN COMMAND
        # -----------------------------
        return {
            "status": "error",
            "output": f"Unknown command: {command}"
        }

    # -----------------------------
    # COMMAND HISTORY
    # -----------------------------
    def get_history(self):
        return self.history