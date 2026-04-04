# AgentForge

AgentForge is an OpenEnv-compliant environment that simulates a real-world software engineering workflow. It allows an AI agent to act as an autonomous developer capable of planning, coding, debugging, testing, and adapting to evolving system conditions.

## Overview

Traditional AI environments are static and limited to single-step problem solving. AgentForge introduces a dynamic and realistic workflow where the agent must interact with multiple tools, handle failures, and respond to changing requirements.

The environment is deterministic, reproducible, and designed for evaluating multi-step reasoning and tool usage.

## Problem Statement

Modern software development involves complex workflows including debugging, testing, and adapting to changing requirements. Most AI environments fail to capture this complexity and remain limited to static problem-solving.

AgentForge addresses this gap by providing a dynamic, tool-integrated environment where agents must continuously adapt and make decisions like real developers.


## Key Features

* OpenEnv-compliant environment with `step()`, `reset()`, and `state()` APIs
* Multi-step task execution (easy, medium, hard, hard_plus)
* Tool-based interaction (code editor, test runner, git, terminal, documentation search)
* Self-diagnosis capability for failure analysis
* Dynamic issue injection to simulate real-world instability
* Reward shaping based on correctness, efficiency, and workflow quality
* Step-by-step reasoning trace and history logging
* Live dashboard with real-time performance tracking

## Real-World Use Cases

* Automating repetitive development workflows in startups and enterprises
* Training AI agents for real-world coding and debugging scenarios
* Benchmarking AI systems on multi-step reasoning tasks
* Simulating software engineering environments for research and testing



## System Architecture

```
Agent (HybridAgent)
        │
        ▼
Environment (AgentForgeEnv)
        │
        ├── State (EnvironmentState)
        ├── Tasks (TaskManager)
        ├── Reward (RewardCalculator)
        ├── Grader (Evaluation)
        │
        ▼
Tools Layer
  ├── Code Editor
  ├── Test Runner
  ├── Git Tool
  ├── Terminal Tool
  ├── Documentation Search
```

## Workflow

1. Agent reads task description
2. Uses documentation search for context
3. Runs tests to identify failures
4. Diagnoses the issue
5. Edits code using tools
6. Re-runs tests to validate fix
7. Handles dynamically injected issues
8. Final evaluation and scoring

## Dynamic Environment

AgentForge simulates real-world instability by injecting new issues even after the agent successfully solves a task. This forces the agent to adapt and re-solve the problem, mimicking real software development conditions.

## Installation

Create a virtual environment and install dependencies:

```
pip install -r requirements.txt
```

## Running the Agent (CLI)

```
python inference.py
```

## Running the Dashboard

```
streamlit run app.py
```

Then open the provided local URL in your browser.

## Configuration

The environment is defined using `openenv.yaml`, which specifies:

* Observation space
* Action space
* Entry point
* Reward range

## Evaluation

The system evaluates the agent based on:

* Correctness (test results)
* Completion
* Workflow efficiency
* Stability under dynamic conditions

## Project Structure

```
agentforge/
│
├── env/
│   ├── environment.py
│   ├── state.py
│   ├── tasks.py
│   ├── reward.py
│   ├── grader.py
│
├── tools/
│   ├── code_editor.py
│   ├── test_runner.py
│   ├── doc_search.py
│   ├── git.py
│   ├── terminal.py
│
├── inference.py
├── app.py
├── openenv.yaml
├── requirements.txt
└── README.md
```

## Design Decisions

* Rule-based agent used for deterministic behavior and zero API dependency
* Simulated tools used for performance and reproducibility
* Modular architecture to allow easy extension and scaling

## Future Improvements

* Integration with real execution environments
* Advanced planning strategies
* Multi-agent collaboration
* Deployment on HuggingFace Spaces

## Business Impact

AgentForge can significantly reduce development time by enabling AI-driven automation of debugging and testing workflows. 

It has potential applications in:
* Developer productivity tools
* AI-assisted coding platforms
* Enterprise workflow automation systems

This makes it valuable for both startups and large-scale tech companies.

## Target Users

* AI researchers and engineers
* Developers building autonomous coding agents
* Organizations exploring AI-driven development workflows


## Conclusion

AgentForge goes beyond static problem-solving environments by introducing dynamic workflows, tool-based reasoning, and adaptive behavior. It provides a realistic benchmark for evaluating autonomous AI agents in software engineering tasks.
