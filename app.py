import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Toolkit", layout="wide")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key="Your API key here"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.title("🤖 AI Toolkit")
tool = st.sidebar.radio("Choose Tool", [
    "Chat Assistant", "Summarizer", "Study Notes", "Planner", "PDF Chat"
])
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []

# CHAT ASSISTANT
if tool == "Chat Assistant":
    st.title("💬 AI Chat Assistant")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Build history string manually
        history = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}"
            for m in st.session_state.messages[:-1]
        )
        prompt = f"Conversation so far:\n{history}\n\nUser: {user_input}\nAI:"
        response = llm.invoke(prompt).content

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# SUMMARIZER
elif tool == "Summarizer":
    st.title("🧠 Text / Code Summarizer")
    text = st.chat_input("Paste text or code to summarize...")
    if text:
        with st.chat_message("user"):
            st.markdown(text)
        response = llm.invoke(f"Summarize this clearly:\n{text}").content
        with st.chat_message("assistant"):
            st.markdown(response)

# STUDY NOTES
elif tool == "Study Notes":
    st.title("📚 Study Notes Generator")
    topic = st.chat_input("Enter topic...")
    if topic:
        with st.chat_message("user"):
            st.markdown(topic)
        response = llm.invoke(f"Create exam-ready notes on: {topic}").content
        with st.chat_message("assistant"):
            st.markdown(response)

# PLANNER
elif tool == "Planner":
    st.title("📅 Daily Planner")
    goals = st.chat_input("Enter your tasks...")
    if goals:
        with st.chat_message("user"):
            st.markdown(goals)
        response = llm.invoke(f"Create a structured daily plan:\n{goals}").content
        with st.chat_message("assistant"):
            st.markdown(response)

# PDF CHAT
elif tool == "PDF Chat":
    st.title("📄 Chat with PDF")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        text = "".join(page.extract_text() or "" for page in pdf_reader.pages)

        if text:
            st.success("PDF loaded! Ask your question below.")
            query = st.chat_input("Ask something about the PDF...")
            if query:
                with st.chat_message("user"):
                    st.markdown(query)
                response = llm.invoke(
                    f"Based on this document:\n{text}\n\nAnswer this: {query}"
                ).content
                with st.chat_message("assistant"):
                    st.markdown(response)
        else:
            st.error("Could not extract text from this PDF.")