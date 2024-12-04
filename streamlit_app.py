import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Set page title
st.title("Pushup Goal Tracker")

# Session state initialization
if "pushup_count" not in st.session_state:
    st.session_state["pushup_count"] = 0
if "goal" not in st.session_state:
    st.session_state["goal"] = 0
if "goal_date" not in st.session_state:
    st.session_state["goal_date"] = datetime.date.today()
if "daily_counts" not in st.session_state:
    st.session_state["daily_counts"] = {}

# Goal setup
st.sidebar.header("Set Your Pushup Goal")
goal = st.sidebar.number_input("Enter total pushup goal:", min_value=1, value=50, step=1)
goal_date = st.sidebar.date_input("Target completion date:", min_value=datetime.date.today())

# Update goal
if st.sidebar.button("Set Goal"):
    st.session_state["goal"] = goal
    st.session_state["goal_date"] = goal_date
    st.session_state["daily_counts"] = {}

# Display goal and progress
st.write(f"**Goal:** {st.session_state['goal']} pushups by {st.session_state['goal_date']}")
st.write(f"**Total Pushups Done:** {st.session_state['pushup_count']}")

# Increment pushup count
if st.button("I Did a Pushup!"):
    st.session_state["pushup_count"] += 1
    today = datetime.date.today()
    if today in st.session_state["daily_counts"]:
        st.session_state["daily_counts"][today] += 1
    else:
        st.session_state["daily_counts"][today] = 1

# Calculate expected pushups
if st.session_state["goal"] > 0:
    total_days = (st.session_state["goal_date"] - datetime.date.today()).days + 1
    expected_daily = st.session_state["goal"] / total_days

    # Prepare data for plotting
    dates = pd.date_range(datetime.date.today(), st.session_state["goal_date"]).to_pydatetime().tolist()
    expected_pushups = [expected_daily * (i + 1) for i in range(len(dates))]
    actual_pushups = [sum(st.session_state["daily_counts"].get(date.date(), 0) for date in dates[:i+1]) for i in range(len(dates))]

    # Plot graph
    fig, ax = plt.subplots()
    ax.plot(dates, expected_pushups, label="Expected Pushups (Cumulative)", color="blue")
    ax.bar(dates, actual_pushups, label="Actual Pushups (Daily Total)", color="orange")
    ax.set_xlabel("Date")
    ax.set_ylabel("Pushups")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.write("Set your goal to see the progress graph.")
