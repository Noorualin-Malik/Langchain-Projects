# llm, tool, agent, memory, streaming, web interface

from langchain_grok import ChatGrok
from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

llm=ChatGrok(model="openai/gpt-oss-20b", streaming=True)
search=GoogleSerperAPIWrapper()
tools=[search.run]

if "memory" not in st.session_state:
    st.session_state.memory=MemorySaver()
    st.session_state.history=[]
    
    
memory=MemorySaver()
agent=create_agent(
    model=llm,
    tools=tools,
    checkpointer=st.session_state.memory,
    system_prompt="You are a amzing agent and can search google as well"
    
)
# print(st.session_state.memory)
# building web inteface
st.subheader("Quick Answer")
for message in st.session_state.history:
    role=message["role"]
    content=message["content"]
    st.chat_message(role).markdown(content)
    
    
query=st.chat_input("Ask Anything? ")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role":"user", "content":"who is pm of pakistan"})
    
    
    response=agent.stream(
        {"messages":[{"role":"user", "content":"who is pm of pakistan"}]},
        {"configurable":{"thread_id":"1"}}
        stream_mode="messages"
    )
    
    ai_container=st.chat_message("ai")
    with ai_container:
        space=st.empty()
        msg= ""
        for chunk in response:
            message= message + chunk[0].content
            space.write(message)
    # answer=response["messages"][-1].content
    # st.chat_message("ai").markdown(answer)
    st.session_state.history.append({"role":"ai", "content":message})

# print(response["messages"][-1].content)