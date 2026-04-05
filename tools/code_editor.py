from typing import Dict


class CodeEditor:
    def __init__(self, files: Dict[str, str]):
        self.files = files

    def create_file(self, filename: str, content: str) -> str:
        if filename in self.files:
            return f"File '{filename}' already exists."
        self.files[filename] = content
        return f"File '{filename}' created."

    def edit_file(self, filename: str, new_content: str) -> str:
        if filename not in self.files:
            return f"File '{filename}' not found."
        self.files[filename] = new_content
        return f"File '{filename}' updated."

    def append_to_file(self, filename: str, content: str) -> str:
        if filename not in self.files:
            return f"File '{filename}' not found."
        self.files[filename] += "\n" + content
        return f"Content appended to '{filename}'."

    def delete_file(self, filename: str) -> str:
        if filename not in self.files:
            return f"File '{filename}' not found."
        del self.files[filename]
        return f"File '{filename}' deleted."

    def read_file(self, filename: str) -> str:
        if filename not in self.files:
            return f"File '{filename}' not found."
        return self.files[filename]