# AgentForge

An OpenEnv-compliant environment that simulates a real-world software engineering workflow for AI agents.

---

## Overview

AgentForge is a structured environment where an agent performs tasks similar to a software engineer:

* Writing and modifying code
* Debugging issues
* Running tests
* Iteratively improving solutions

The environment is designed to evaluate multi-step reasoning, tool usage, and decision-making.

---

## Features

* Multi-tool simulation (code editor, test runner)
* Step-based environment following OpenEnv principles
* Reward-driven evaluation
* Deterministic and reproducible execution
* Multiple task levels (easy, medium, hard)
* Hybrid agent support (rule-based with optional OpenAI integration)

---

## Architecture

Agent → Action → Environment → Tools → State Update → Reward

### Components

* `env/` — core environment logic (state, tasks, reward, execution)
* `tools/` — tool simulation layer
* `inference.py` — agent execution loop
* `openenv.yaml` — environment configuration

---

## Tasks

### Easy

Fix a bug in a simple function.

### Medium

Refactor multi-file code and handle edge cases.

### Hard

Implement a feature with evolving requirements and optimize performance.

---

## How to Run

### 1. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the System

```bash
python inference.py
```

---

## Output

The system provides:

* Step-by-step agent actions
* Tool execution results
* Reward per step
* Final score and step count

---

## Agent Design

* Default: rule-based agent (deterministic and stable)
* Optional: OpenAI-based decisions (if API key is provided)
* Automatic fallback ensures uninterrupted execution

---

## Docker

```bash
docker build -t agentforge .
docker run agentforge
```

---

## Notes

* Works without API key
* OpenAI integration is optional
* Designed for reproducibility
* Compatible with low-resource environments

---

## Project Structure

```
agentforge/
│
├── env/
├── tools/
├── inference.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

Built for OpenEnv Hackathon
