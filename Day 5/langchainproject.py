import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

# ========== 1. API Key ==========
GOOGLE_API_KEY = "AIzaSyAYbFP5MMt_qm5sgtrzlysXRWxxqZ6uKqo"  # Replace with your actual Gemini API key

# ========== 2. Streamlit UI ==========
st.set_page_config(page_title="English to French Translator", layout="centered")
st.title("🌍 English to French Translator")
st.markdown("Enter an English sentence, and the AI will translate it to French.")

# Input box
english_text = st.text_input("Enter English Sentence:", placeholder="e.g., How are you?")

# Translate button
if st.button("Translate"):
    if not english_text.strip():
        st.warning("⚠️ Please enter a sentence to translate.")
    else:
        try:
            # ========== 3. LangChain Setup ==========
            llm = ChatGoogleGenerativeAI(
                model="models/gemini-2.0-flash",  # Use a valid model
                temperature=0.3,
                google_api_key=GOOGLE_API_KEY  # Key passed directly in code
            )

            # ========== 4. Prompt Template ==========
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant that translates English sentences to French."),
                ("user", "Translate this sentence to French: {text}")
            ])

            # ========== 5. Create Chain ==========
            chain: Runnable = prompt | llm

            # Run chain
            response = chain.invoke({"text": english_text})

            # Get the output text
            french_translation = response.content if hasattr(response, "content") else str(response)

            # ========== 6. Output ==========
            st.success("✅ Translation Successful!")
            st.markdown(f"**French Translation:**\n\n> {french_translation}")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
