from typing import Dict, Any, List
from datetime import datetime
import copy


class GitTool:
    def __init__(self):
        self.commits: List[Dict[str, Any]] = []

    # -----------------------------
    # COMMIT CHANGES
    # -----------------------------
    def commit(self, state, message: str) -> Dict[str, Any]:
        if not state.files:
            return {
                "status": "failed",
                "message": "No files to commit"
            }

        commit_data = {
            "id": f"commit_{len(self.commits) + 1}",
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "files_snapshot": copy.deepcopy(state.files)
        }

        self.commits.append(commit_data)

        return {
            "status": "success",
            "commit_id": commit_data["id"],
            "message": message,
            "total_commits": len(self.commits)
        }

    # -----------------------------
    # GET COMMIT HISTORY
    # -----------------------------
    def log(self) -> Dict[str, Any]:
        return {
            "total_commits": len(self.commits),
            "history": [
                {
                    "id": c["id"],
                    "message": c["message"],
                    "timestamp": c["timestamp"]
                }
                for c in self.commits
            ]
        }

    # -----------------------------
    # RESET TO PREVIOUS COMMIT
    # -----------------------------
    def checkout(self, state, commit_id: str) -> Dict[str, Any]:
        for commit in self.commits:
            if commit["id"] == commit_id:
                state.files = copy.deepcopy(commit["files_snapshot"])
                return {
                    "status": "success",
                    "message": f"Checked out to {commit_id}"
                }

        return {
            "status": "failed",
            "message": "Commit not found"
        }