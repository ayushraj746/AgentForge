import streamlit as st
import time
import pandas as pd

from env.environment import AgentForgeEnv
from inference import HybridAgent

st.set_page_config(page_title="AgentForge", layout="wide")

# ---------------- STYLE ---------------- #
st.markdown("""
<style>
.block-container {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.title("AgentForge Dashboard")
st.caption("Autonomous Software Engineering Agent")

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

    # Layout
    col1, col2, col3 = st.columns(3)

    reward_placeholder = col1.empty()
    step_placeholder = col2.empty()
    status_placeholder = col3.empty()

    progress = st.progress(0)

    total_reward = 0.0

    # 🔥 Chart tracking
    reward_history = []
    step_history = []

    log_area = st.container()

    # 🔥 Live chart placeholder
    chart_placeholder = st.empty()

    # ---------------- LOOP ---------------- #
    for step in range(20):
        progress.progress((step + 1) / 20)

        action = agent.decide_action(state)
        result = env.step(action)

        state = result["state"]
        reward = result["reward"]
        done = result["done"]

        total_reward += reward

        # store for chart
        reward_history.append(total_reward)
        step_history.append(step + 1)

        # ---------------- METRICS ---------------- #
        reward_placeholder.metric("Total Reward", round(total_reward, 3))
        step_placeholder.metric("Steps", step + 1)
        status_placeholder.metric("Status", "Running")

        # ---------------- LIVE CHART ---------------- #
        df = pd.DataFrame({
            "Step": step_history,
            "Reward": reward_history
        }).set_index("Step")

        chart_placeholder.line_chart(df)

        # ---------------- LOGS ---------------- #
        with log_area:
            with st.expander(f"Step {step+1}", expanded=False):
                st.write("🧠 Reasoning:", action.get("reasoning"))
                st.write("⚡ Action:", action)
                st.write("📌 Result:", result["result"])
                st.write("💰 Reward:", reward)

                if "Diagnosis" in str(action.get("reasoning")):
                    st.info("🧠 Diagnosis triggered")

                if "Dynamic Issue" in str(result["result"]) or "Dynamic Issue" in str(result):
                    st.warning("⚠️ Dynamic Issue Injected")

        if done:
            status_placeholder.metric("Status", "Completed")
            st.success("Task Completed Successfully")
            break

        time.sleep(0.3)

    # ---------------- FINAL ---------------- #
    st.divider()

    evaluation = env.evaluate()

    colA, colB = st.columns(2)

    with colA:
        st.subheader("Evaluation")
        st.json(evaluation)

    with colB:
        st.subheader("Tool Usage")
        st.json(state.get("tool_usage"))

    st.subheader("Reasoning Trace")
    st.write(state.get("reasoning_trace"))