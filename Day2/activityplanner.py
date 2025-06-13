import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ---------- Session State Initialization ----------
if 'activity_log' not in st.session_state:
    st.session_state.activity_log = []

if 'completed_today' not in st.session_state:
    st.session_state.completed_today = False

# ---------- Creative Suggestions ----------
def suggest_creative_activities(duration):
    suggestions = {
        15: ["Draw a rainbow", "Make paper boats", "Color a fruit picture"],
        30: ["Build with blocks", "Learn a dance", "Do a puzzle"],
        45: ["Create a storybook", "Craft with leaves", "Paint with watercolor"],
        60: ["Lego challenge", "Origami session", "Simple science experiment"]
    }
    return suggestions.get(duration, ["Read a picture book", "Nature walk", "Clay modeling"])

# ---------- Activity Input Form ----------
st.title("🧒 Daily Planner for Kids (4+ Years)")
st.subheader("Enter today's routine")

with st.form("activity_form"):
    date = st.date_input("Date", datetime.today())
    homework_time = st.slider("Time spent on homework (in minutes)", 0, 180, 30, 5)
    extracurricular_time = st.slider("Time for extracurriculars (music, dance, etc.)", 0, 180, 30, 5)
    creative_time = st.slider("Time available for creative activities", 0, 60, 15, 15)
    submitted = st.form_submit_button("Suggest Activities & Save")

# ---------- Processing Input ----------
if submitted and not st.session_state.completed_today:
    suggestions = suggest_creative_activities(creative_time)
    st.success("Suggested Creative Activities:")
    for act in suggestions:
        st.write(f"👉 {act}")

    entry = {
        "date": date,
        "homework_time": homework_time,
        "extracurricular_time": extracurricular_time,
        "creative_time": creative_time,
        "suggested": suggestions
    }
    st.session_state.activity_log.append(entry)
    st.session_state.completed_today = True

# ---------- Daily Summary ----------
st.markdown("## 📅 Daily Summary")
if st.session_state.activity_log:
    df = pd.DataFrame(st.session_state.activity_log)
    df['date'] = pd.to_datetime(df['date'])

    latest = df[df['date'] == df['date'].max()].iloc[-1]
    st.write(f"**Date:** {latest['date'].date()}")
    st.write(f"**Homework:** {latest['homework_time']} mins")
    st.write(f"**Extracurricular:** {latest['extracurricular_time']} mins")
    st.write(f"**Creative Time:** {latest['creative_time']} mins")
    st.write("**Suggested Activities:**")
    for act in latest['suggested']:
        st.write(f"✔️ {act}")
else:
    st.info("No activity added yet.")

# ---------- Weekly / Monthly Summary ----------
st.markdown("## 📊 Weekly/Monthly Activity Summary")

if len(st.session_state.activity_log) >= 1:
    df = pd.DataFrame(st.session_state.activity_log)
    df['date'] = pd.to_datetime(df['date'])

    time_filter = st.radio("Show summary for", ["Last 7 days", "Last 30 days"])
    days = 7 if time_filter == "Last 7 days" else 30
    cutoff = datetime.today() - timedelta(days=days)

    filtered_df = df[df['date'] >= cutoff]

    if not filtered_df.empty:
        summary = filtered_df[["homework_time", "extracurricular_time", "creative_time"]].sum()

        # Bar Chart
        fig, ax = plt.subplots()
        summary.plot(kind='bar', ax=ax, color=['blue', 'green', 'orange'])
        ax.set_ylabel("Time in Minutes")
        ax.set_title(f"Total Time Spent in Activities ({time_filter})")
        st.pyplot(fig)
    else:
        st.warning("No data available for selected time range.")

# ---------- Download Option ----------
st.markdown("## 📥 Download Log")
if st.session_state.activity_log:
    export_df = pd.DataFrame(st.session_state.activity_log)
    st.download_button("Download as CSV", export_df.to_csv(index=False), file_name="child_activities.csv")
