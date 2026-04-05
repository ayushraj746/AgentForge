from typing import Dict


class DocSearchTool:
    def __init__(self):
        # Simulated documentation database
        self.docs = {
            "sum": "To sum numbers, iterate over list and accumulate total using a loop or use built-in sum().",
            "list": "Lists in Python are ordered collections. Always validate input before processing.",
            "validate": "Validation should check type, None values, and empty cases.",
            "error": "Check stack trace and handle edge cases like None or invalid input.",
            "divide": "Always handle division by zero using conditional checks.",
            "performance": "Optimize by reducing loops and using built-in functions.",
            "max": "Use max() to find largest element in a list.",
        }

    def search(self, query: str) -> Dict:
        query = query.lower()

        results = []

        for keyword, content in self.docs.items():
            if keyword in query:
                results.append({
                    "keyword": keyword,
                    "content": content
                })

        # fallback if nothing found
        if not results:
            results.append({
                "keyword": "general",
                "content": "No direct match found. Try checking function logic, input validation, and edge cases."
            })

        return {
            "query": query,
            "results": results
        }