import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import SerpAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI

# ===== Streamlit Page Setup =====
st.set_page_config(page_title="🧠 Job Finder Bot", layout="centered")
st.title("💼 Real-Time Job Finder Bot")
st.markdown("🔍 Ask about **latest job vacancies** based on your skills. Powered by Gemini + Google Jobs via SerpAPI!")

# ===== Input Field =====
skill_query = st.text_input("🛠️ Enter your skill or job role:", placeholder="e.g., Python Developer, Data Analyst")

# ===== Button Trigger =====
search_button = st.button("🔎 Find Jobs")

# ===== Error/Response Display =====
response_area = st.empty()

# ===== API and Model Setup =====
try:
    # Initialize Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key="AIzaSyAYbFP5MMt_qm5sgtrzlysXRWxxqZ6uKqo",
        temperature=0.3
    )

    # Initialize SerpAPIWrapper (without gl and hl)
    serpapi = SerpAPIWrapper(
        serpapi_api_key="6345f496ff9349f2e37d9f7cdbf0b062f0ac194626b75f3d170fe88fb8afb11e"  # Replace with your actual SerpAPI key
    )

    tools = [
        Tool(
            name="Job Search via Google",
            func=serpapi.run,
            description="Useful for finding the latest job openings and listings based on specific skills or job roles."
        )
    ]

    # Initialize the agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        handle_parsing_errors=True
    )

except Exception as e:
    st.error(f"❌ Error setting up the LLM or tools: {e}")

# ===== Process User Query =====
if search_button and skill_query:
    try:
        query = f"Show latest job listings and companies hiring today for: {skill_query}"
        with st.spinner("🔄 Fetching real-time job listings..."):
            result = agent.run(query)
        response_area.success("✅ Here's what I found:")
        response_area.markdown(result)

    except Exception as err:
        response_area.error(f"⚠️ Oops! Something went wrong: {err}")

elif search_button and not skill_query:
    response_area.warning("⚠️ Please enter a skill or job role to search.")
