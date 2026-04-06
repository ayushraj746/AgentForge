import streamlit as st
import time
import pandas as pd
import threading

# ===== FASTAPI IMPORTS =====
from fastapi import FastAPI
import uvicorn

from env.environment import AgentForgeEnv
from inference import HybridAgent

# ============================
# FASTAPI BACKEND (FOR HACKATHON)
# ============================

api = FastAPI()

env = AgentForgeEnv()
agent = HybridAgent()
state = None

@api.get("/")
def root():
    return {"message": "AgentForge API running"}

@api.get("/health")
def health():
    return {"status": "ok"}

@api.post("/reset")
def reset(task: str = "easy"):
    global state
    state = env.reset(task=task)
    return {"state": state}

@api.post("/step")
def step():
    global state
    action = agent.decide_action(state)
    result = env.step(action)
    state = result["state"]
    return result

# ============================
# RUN FASTAPI IN BACKGROUND
# ============================

def run_api():
    uvicorn.run(api, host="0.0.0.0", port=7860)

if "api_started" not in st.session_state:
    threading.Thread(target=run_api, daemon=True).start()
    st.session_state.api_started = True

# ============================
# STREAMLIT UI (UNCHANGED)
# ============================

st.set_page_config(page_title="AgentForge Dashboard", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)

st.title("🚀 AgentForge Dashboard")
st.caption("Autonomous AI Agent for Software Engineering Workflows")

st.sidebar.header("⚙️ Controls")

task = st.sidebar.selectbox(
    "Select Task Difficulty",
    ["easy", "medium", "hard", "hard_plus"]
)

run_button = st.sidebar.button("▶ Run Agent")

if run_button:
    env = AgentForgeEnv()
    agent = HybridAgent()

    state = env.reset(task=task)

    st.subheader(f"📌 Selected Task: {task}")
    st.write("### Task Description")
    st.write(state["current_task"])

    col1, col2, col3 = st.columns(3)

    reward_placeholder = col1.empty()
    step_placeholder = col2.empty()
    status_placeholder = col3.empty()

    progress = st.progress(0)
    total_reward = 0.0

    reward_history = []
    step_history = []

    log_area = st.container()
    chart_placeholder = st.empty()

    for step in range(20):
        progress.progress((step + 1) / 20)

        action = agent.decide_action(state)
        result = env.step(action)

        state = result["state"]
        reward = result["reward"]
        done = result["done"]

        total_reward += reward

        reward_history.append(total_reward)
        step_history.append(step + 1)

        reward_placeholder.metric("💰 Total Reward", round(total_reward, 3))
        step_placeholder.metric("📍 Steps", step + 1)
        status_placeholder.metric("📡 Status", "Running")

        df = pd.DataFrame({
            "Step": step_history,
            "Reward": reward_history
        }).set_index("Step")

        chart_placeholder.line_chart(df)

        with log_area:
            with st.expander(f"Step {step + 1} Details", expanded=False):
                st.write("🧠 Reasoning:", action.get("reasoning"))
                st.write("⚡ Action Taken:", action)
                st.write("📤 Result:", result.get("result"))
                st.write("🎯 Reward Gained:", reward)

        if done:
            status_placeholder.metric("📡 Status", "Completed")
            st.success("✅ Task Completed Successfully")
            break

        time.sleep(0.3)

    st.divider()

    evaluation = env.evaluate()

    colA, colB = st.columns(2)

    with colA:
        st.subheader("📊 Evaluation Results")
        st.json(evaluation)

    with colB:
        st.subheader("🛠 Tool Usage Summary")
        st.json(state.get("tool_usage"))

        st.subheader("🧠 Reasoning Trace")
        st.write(state.get("reasoning_trace"))