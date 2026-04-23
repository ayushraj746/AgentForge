---
title: AgentForge
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# AgentForge

AgentForge is an OpenEnv-compliant environment that simulates a real-world software engineering workflow. It enables an AI agent to act as an autonomous developer capable of planning, coding, debugging, testing, and adapting to dynamic system conditions.

---

# Live API (Hugging Face Deployment)

Base URL:

```
https://ayush746-agentforge.hf.space
```

### Available Endpoints

* `GET /` — API status
* `GET /health` — Health check
* `POST /reset` — Initialize task
* `POST /step` — Execute agent step
* `GET /state` — Current state
* `GET /evaluate` — Final evaluation

Interactive API docs:

```
/docs
```

---

# Overview

Traditional AI environments are static and limited to single-step problem solving.

AgentForge introduces a dynamic, tool-integrated workflow where the agent must:

* interact with multiple tools
* handle failures
* adapt to changing requirements

The environment is deterministic, reproducible, and designed for evaluating multi-step reasoning and tool usage.

---

# Problem Statement

Modern software development involves:

* debugging
* testing
* adapting to evolving requirements

Most AI environments fail to capture this complexity.

AgentForge addresses this gap by simulating a realistic developer workflow.

---

# Key Features

* OpenEnv-compliant APIs (`reset()`, `step()`, `state()`)
* Multi-step tasks (easy to hard_plus)
* Tool-based interaction:

  * Code Editor
  * Test Runner
  * Git
  * Terminal
  * Documentation Search
* Self-diagnosis capability
* Dynamic issue injection
* Reward shaping
* Full reasoning trace
* Streamlit-based dashboard (local)

---

# API Usage (Evaluation)

### Reset Environment

```
POST /reset
```

Response:

```json
{
  "state": {...}
}
```

---

### Execute Step

```
POST /step
```

Response:

```json
{
  "state": {...},
  "reward": float,
  "done": bool
}
```

---

# System Architecture

```
Agent (HybridAgent)
        │
        ▼
Environment (AgentForgeEnv)
        │
        ├── State
        ├── Tasks
        ├── Reward
        ├── Evaluation
        │
        ▼
Tools Layer
  ├── Code Editor
  ├── Test Runner
  ├── Git Tool
  ├── Terminal Tool
  ├── Documentation Search
```

---

# Workflow

1. Read task
2. Search documentation
3. Run tests
4. Diagnose issue
5. Modify code
6. Validate fix
7. Handle dynamic issues
8. Final evaluation

---

# Dynamic Environment

AgentForge injects new issues even after a task is solved, forcing continuous adaptation and mimicking real-world engineering conditions.

---

# Running Locally

### Install dependencies

```
pip install -r requirements.txt
```

### Run Agent (CLI)

```
python inference.py
```

### Run Dashboard (UI)

```
streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

# Project Structure

```
agentforge/
│
├── env/
├── tools/
├── api.py          # FastAPI backend (HF deployment)
├── app.py          # Streamlit UI (local demo)
├── inference.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Design Decisions

* Rule-based agent for deterministic behavior
* Simulated tools for performance and reproducibility
* Modular architecture for extensibility

---

# Future Improvements

* Integration with real execution environments
* Advanced planning strategies
* Multi-agent collaboration

---

# Business Impact

AgentForge can enable:

* AI-driven debugging workflows
* automated development pipelines
* developer productivity tools

---

# Target Users

* AI researchers
* ML engineers
* developers building autonomous agents
* organizations exploring AI-driven workflows

---

# Conclusion

AgentForge transforms static AI environments into dynamic, tool-driven systems, providing a realistic benchmark for autonomous software engineering agents.

---

# Submission Note

This project is OpenEnv-compatible and deployed using Docker on Hugging Face Spaces.

The backend API supports multi-step agent evaluation and is ready for automated testing.
# My profil 
I am vivek Gupta 
Roll No : 0278
Course : BCom (Hons)
Subject: Business Analytics 
