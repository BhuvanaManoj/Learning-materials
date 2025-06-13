import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import tempfile

# ========== Configuration ==========
GOOGLE_API_KEY = "AIzaSyAYbFP5MMt_qm5sgtrzlysXRWxxqZ6uKqo"  # 🔐 Replace with your actual key

# ========== UI Setup ==========
st.set_page_config(page_title="📄 RAG Paper Finder", layout="centered")
st.title("📄 Research Paper Finder using Gemini + RAG")
st.markdown("Upload a research paper (PDF) and enter your **area of interest** to search related content.")

# ========== Upload PDF ==========
pdf_file = st.file_uploader("Upload a PDF document (journal/research paper)", type=["pdf"])

# ========== Input field ==========
query = st.text_input("Enter your area of interest:", placeholder="e.g., Generative AI in Healthcare")

# ========== Search Button ==========
if st.button("🔍 Search"):

    if not pdf_file or not query:
        st.warning("⚠️ Please upload a PDF and enter a topic.")
    else:
        try:
            # ✅ Save uploaded PDF to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(pdf_file.read())
                tmp_file_path = tmp_file.name

            # ========== Load PDF ==========
            loader = PyPDFLoader(tmp_file_path)
            pages = loader.load()

            # ========== Split Text ==========
            splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = splitter.split_documents(pages)

            # ========== Embeddings & FAISS ==========
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
            retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

            # ========== LangChain Memory ==========
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )

            # ========== Custom Prompt ==========
            prompt = ChatPromptTemplate.from_template(
                "You are a research assistant. Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion:\n{question}"
            )

            # ========== LLM Setup (Gemini Flash) ==========
            llm = ChatGoogleGenerativeAI(
                model="models/gemini-2.0-flash",
                google_api_key=GOOGLE_API_KEY,
                temperature=0.3
            )

            # ========== RAG Chain ==========
            rag_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=retriever,
                memory=memory,
                combine_docs_chain_kwargs={"prompt": prompt}
            )

            # ========== Invoke the Chain ==========
            result = rag_chain.invoke({"question": query})

            # ========== Display Result ==========
            st.success("✅ Relevant content found!")
            st.markdown("### 🔗 Extracted Insights")
            st.write(result['answer'])

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

