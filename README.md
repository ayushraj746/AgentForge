# AgentForge — Autonomous Workflow Engineering Environment

AgentForge is an OpenEnv-compatible environment that simulates a real-world software engineering workflow.
It allows an AI agent to act as an autonomous engineer capable of writing code, debugging, testing, and managing tools inside a controlled, evolving system.

---

## Overview

Traditional environments focus on solving isolated problems. AgentForge shifts the focus to **long-running workflows**, where the agent must:

* Understand tasks
* Modify code
* Run tests
* Debug issues
* Use tools effectively
* Adapt to changing requirements

The environment is deterministic, reproducible, and designed for evaluating tool-using AI agents.

---

## Key Features

* Multi-tool interaction (code editor, test runner, documentation search, git, terminal)
* Dynamic environment with evolving requirements and system issues
* Workflow-based agent behavior instead of single-step problem solving
* Multi-signal reward system (correctness, efficiency, progress, penalties)
* Structured grading system for final evaluation
* Full reasoning trace for explainability

---

## Architecture

```id="arch1"
Agent
  ↓
Environment (AgentForgeEnv)
  ↓
State (memory + workflow tracking)
  ↓
Tools (editor, tests, docs, git, terminal)
  ↓
Event Engine (dynamic changes)
  ↓
Reward System (step-level feedback)
  ↓
Grader (final evaluation)
```

---

## Project Structure

```id="struct1"
agentforge/
│
├── env/
│   ├── environment.py   # Core orchestration logic
│   ├── state.py         # Environment state and memory
│   ├── tasks.py         # Task definitions (easy → hard+)
│   ├── reward.py        # Reward calculation
│   ├── grader.py        # Final evaluation
│
├── tools/
│   ├── code_editor.py
│   ├── test_runner.py
│   ├── doc_search.py
│   ├── git.py
│   ├── terminal.py
│
├── inference.py         # Agent logic
├── openenv.yaml         # Environment specification
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Environment Workflow

1. **Reset**

   * Loads a task with initial files and constraints

2. **Step Execution**

   ```id="loop1"
   while not done:
       action = agent.decide(state)
       state, reward = env.step(action)
   ```

3. **Dynamic Events**

   * Requirements may change during execution
   * New issues may appear
   * Dependencies may break

4. **Final Evaluation**

   ```id="eval1"
   result = env.evaluate()
   ```

---

## Agent Design

### Hybrid Agent

* Rule-based (default, stable)
* Optional LLM integration (via OpenAI API)
* Automatic fallback to ensure reliability

### Workflow Behavior

```id="workflow1"
Understand → Test → Debug → Fix → Validate → Commit → Inspect
```

---

## Available Tools

| Tool        | Purpose                         |
| ----------- | ------------------------------- |
| code_editor | File creation and modification  |
| test_runner | Execute test cases              |
| doc_search  | Retrieve relevant documentation |
| git         | Commit and track changes        |
| terminal    | Simulated command execution     |

---

## Reward System

The reward function combines multiple signals:

```id="reward1"
reward =
    correctness
  + efficiency
  + tool_usage
  + progress
  - penalties
```

This encourages:

* correct solutions
* minimal steps
* proper use of tools
* consistent progress

---

## Grading System

Final evaluation score ranges from 0 to 1 and considers:

* correctness
* completion
* workflow quality
* system stability

```id="grade1"
final_score = weighted_sum(metrics)
```

---

## Dynamic Event System

The environment evolves during execution:

| Event Type         | Effect                |
| ------------------ | --------------------- |
| Requirement Change | Modifies task goals   |
| Performance Issue  | Adds constraints      |
| Dependency Break   | Introduces new errors |

---

## Running the Project

```bash id="run1"
python inference.py
```

This executes all tasks:

* easy
* medium
* hard
* hard_plus

---

## Example Execution

```id="example1"
Step 1: doc_search → understand task
Step 2: run_tests → detect failure
Step 3: edit_file → fix issue
Step 4: run_tests → pass
Step 5: git_commit → save changes

Final Score: 0.85
```

---

## OpenEnv Compliance

AgentForge follows OpenEnv requirements:

* step() API
* reset() API
* structured state representation
* defined action and observation spaces
* deterministic execution

---

## Deployment

### Docker

```bash id="docker1"
docker build -t agentforge .
docker run agentforge
```

### HuggingFace (optional)

Can be deployed as:

* evaluation environment
* agent benchmarking setup

---

## Use Cases

* evaluating autonomous coding agents
* studying tool usage behavior
* simulating real engineering workflows
* benchmarking decision-making systems

---

## Future Improvements

* interactive UI (Streamlit)
* multi-agent collaboration
* real API integrations
* more complex task pipelines

---

## Summary

AgentForge is designed as a controlled environment for studying how AI agents operate in realistic software engineering workflows.

It moves beyond isolated tasks and focuses on **end-to-end execution, tool usage, and system-level reasoning**.
