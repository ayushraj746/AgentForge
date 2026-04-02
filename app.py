import streamlit as st
import time

from env.environment import AgentForgeEnv
from inference import HybridAgent

st.set_page_config(page_title="AgentForge", layout="wide")

st.title("AgentForge — Autonomous Software Engineering Agent")

# ---------------- SIDEBAR ---------------- #
st.sidebar.header("Controls")

task = st.sidebar.selectbox(
    "Select Task",
    ["easy", "medium", "hard", "hard_plus"]
)

run_button = st.sidebar.button("Run Agent")

# ---------------- MAIN ---------------- #
if run_button:
    env = AgentForgeEnv()
    agent = HybridAgent()

    state = env.reset(task=task)

    st.subheader(f"Task: {task}")
    st.write(state["current_task"])

    total_reward = 0.0

    step_container = st.container()

    for step in range(20):
        with step_container:
            st.markdown(f"### Step {step+1}")

            action = agent.decide_action(state)

            st.write("🧠 Reasoning:", action.get("reasoning"))
            st.write("⚡ Action:", action)

            result = env.step(action)

            state = result["state"]
            reward = result["reward"]
            done = result["done"]

            total_reward += reward

            st.write("📌 Result:", result["result"])
            st.write("💰 Reward:", reward)

            # Highlight dynamic issue
            if "Dynamic Issue Injected" in str(result["result"]) or "Dynamic Issue" in str(result):
                st.warning("⚠️ Dynamic Issue Triggered")

            if done:
                st.success("Task Completed")
                break

            time.sleep(0.3)

    # ---------------- FINAL ---------------- #
    evaluation = env.evaluate()

    st.subheader("Final Evaluation")
    st.write(evaluation)

    st.subheader("Total Reward")
    st.write(total_reward)

    st.subheader("Tool Usage")
    st.write(state.get("tool_usage"))

    st.subheader("Reasoning Trace")
    st.write(state.get("reasoning_trace"))