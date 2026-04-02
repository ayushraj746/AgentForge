from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

from env.environment import AgentForgeEnv

app = FastAPI()
env = AgentForgeEnv()


class ActionRequest(BaseModel):
    tool: str
    params: Dict[str, Any] = {}
    reasoning: str = ""


@app.get("/")
def root():
    return {"message": "AgentForge API running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset(task: str = "easy"):
    return env.reset(task)


@app.post("/step")
def step(action: ActionRequest):
    return env.step(action.model_dump())


@app.get("/state")
def state():
    return env.get_state()


@app.get("/evaluate")
def evaluate():
    return env.evaluate()


@app.post("/run")
def run(task: str = "easy", max_steps: int = 20):
    from inference import run_episode
    score = run_episode(task, max_steps)
    return {"task": task, "score": score}