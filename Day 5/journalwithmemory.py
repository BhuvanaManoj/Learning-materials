import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
import tempfile

# ========== Configuration ==========
GOOGLE_API_KEY = "AIzaSyAYbFP5MMt_qm5sgtrzlysXRWxxqZ6uKqo"  # 🔐 Your actual key

# ========== UI Setup ==========
st.set_page_config(page_title="🧠 Gemini RAG Chat", layout="centered")
st.title("🧠 Research Chat with Gemini + RAG")
st.markdown("Upload a research paper and chat with the assistant. The model remembers the conversation!")

# ========== Upload PDF ==========
pdf_file = st.file_uploader("📄 Upload a research paper (PDF)", type=["pdf"])

# ========== Setup Memory ==========
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

# ========== PDF Processing ==========
if pdf_file and not st.session_state.rag_chain:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_file_path = tmp_file.name

    loader = PyPDFLoader(tmp_file_path)
    pages = loader.load()

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(pages)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Gemini LLM setup
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.0-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.3
    )

    # Prompt templates
    qa_prompt = ChatPromptTemplate.from_template(
        "You are a research assistant. Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion:\n{question}"
    )
    condense_prompt = ChatPromptTemplate.from_template(
        "Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question.\n\nChat History:\n{chat_history}\n\nFollow-Up Question:\n{question}"
    )

    question_generator = LLMChain(llm=llm, prompt=condense_prompt)
    doc_chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=qa_prompt)

    rag_chain = ConversationalRetrievalChain(
        retriever=retriever,
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        memory=st.session_state.memory
    )

    st.session_state.rag_chain = rag_chain
    st.success("✅ PDF processed and RAG chain is ready. You can now start chatting below!")

# ========== Chat Interface ==========
if st.session_state.rag_chain:
    user_input = st.chat_input("Ask your question about the paper...")

    if user_input:
        result = st.session_state.rag_chain.invoke({"question": user_input})
        st.session_state.memory.chat_memory.add_user_message(user_input)
        st.session_state.memory.chat_memory.add_ai_message(result['answer'])

    # Display chat history
    for msg in st.session_state.memory.chat_memory.messages:
        if msg.type == "human":
            st.chat_message("user").markdown(msg.content)
        elif msg.type == "ai":
            st.chat_message("assistant").markdown(msg.content)
