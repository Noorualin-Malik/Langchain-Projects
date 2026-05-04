# =========================
# IMPORTS
# =========================
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver


# =========================
# DATABASE SETUP (FIXED)
# =========================
DB_PATH = "E:/practice_youtube/apps/my_tasks.db"

print("DB EXISTS:", os.path.exists(DB_PATH))

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False}
)

db = SQLDatabase(engine)


# Create table safely
db.run("""
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK (status IN ('pending', 'in progress', 'completed')) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")


# =========================
# MODEL
# =========================

model = ChatGroq(model="openai/gpt-oss-20b")


# =========================
# TOOLKIT
# =========================


toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()


# =========================
# SYSTEM PROMPT (FIXED - NOT TOO STRICT)
# =========================
system_prompt = """
You are a SQL assistant for a task management system.

RULES:
- Convert user requests into SQL queries using tools.
- Always use tasks table.
- Limit SELECT results to 10.
- Order SELECT by created_at DESC.
- Do NOT use comments in SQL.
- If unclear, assume user wants to view tasks.

TABLE:
tasks(id, title, description, status, created_at)
"""


# =========================
# AGENT
# =========================
@st.cache_resource
def get_agent():
    return create_react_agent(
        model=model,
        tools=tools,
        checkpointer=InMemorySaver(),
        prompt=system_prompt
    )

agent = get_agent()


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="TaskBot", page_icon="🧠")
st.title("🧠 TaskBot - AI Task Manager")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "user-session-1"


# show chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])


# input
prompt = st.chat_input("Ask me to manage your tasks...")

if prompt:

    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            response = agent.invoke(
                {"messages": [{"role": "user", "content": prompt}]},
                {"configurable": {"thread_id": st.session_state.thread_id}}
            )

            result = response["messages"][-1].content

            st.markdown(result)

            st.session_state.messages.append(
                {"role": "assistant", "content": result}
            )

    print("AI:", result)