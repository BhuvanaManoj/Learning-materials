import streamlit as st
import requests
from datetime import datetime

# ==========================
# CONFIGURATION
# ==========================
N8N_WEBHOOK_URL = "https://bhuvaneswari.app.n8n.cloud/webhook-test/77ab91d2-4b35-4d0b-ac81-8b6dfffe2d1d"  # Replace with your actual n8n webhook URL

# ==========================
# UI - Mentor Session Log Form
# ==========================
st.title("📝 Mentor Session Log")

with st.form("session_log_form"):
    st.subheader("Mentorship Session Details")

    mentor_id = st.text_input("Mentor ID or Name")
    mentee_id = st.text_input("Mentee ID or Name")
    session_date = st.date_input("Session Date", value=datetime.today())
    session_notes = st.text_area("Session Summary / Notes", height=200)
    goal_progress = st.slider("Goal Completion (%)", 0, 100, 0, step=5)

    submitted = st.form_submit_button("Submit Session Log")

    if submitted:
        if not mentor_id or not mentee_id or not session_notes:
            st.warning("Please fill in all the required fields.")
        else:
            payload = {
                "mentor_id": mentor_id,
                "mentee_id": mentee_id,
                "session_date": str(session_date),
                "notes": session_notes,
                "goal_progress": goal_progress
            }

            try:
                response = requests.post(N8N_WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    st.success("✅ Session log submitted successfully!")
                else:
                    st.error(f"❌ Failed to submit. Status Code: {response.status_code}")
            except Exception as e:
                st.error(f"🚫 Error sending data: {e}")
