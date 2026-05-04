# python, langchian, google_gemini, streamlit
# with streamlit, first code
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
# que= "who is PM of Pakistan?"


st.title("Chat Bot")
st.markdown("My QnA bot with Langchain and gemini")


if "messages" not in st.session_state:
    st.session_state.messages=[]
    
# Creates chat memory.
# session_state stores messages so chat doesn't disappear on refresh.
# If no messages exist → create empty list.

for message in st.session_state.messages:
# Loops through previous chat messages.
    role=message["role"]
# Gets who sent the message (user or ai).
    content=message["content"]
# Gets the actual message text.
    st.chat_message(role).markdown(content)
# Displays each message in chat UI
# role decides left/right position (user vs AI)

query=st.chat_input("How can i help you?")

if query:
    st.session_state.messages.append({"role":"user", "content":query})
# Saves user message in chat history.

    st.chat_message("user").markdown(query)
# Displays user's message immediately.
    res=llm.invoke(query)
    
    
    st.chat_message("ai").markdown(res.content)
    
    st.session_state.messages.append({"role":"ai", "content":res.content})
    
    
# task:  Add Clear Chat Button,   Add Loading Spinner
# Task: Improve the chatbot you created in class.

# Requirements:

# 1. Change title and description
# 2. Add sidebar information
# 3. Add clear chat button
# 4. Add system prompt (Python teacher)
# 5. Add loading spinner

# Submit your working Streamlit code.

# from dotenv import load_dotenv
# load_dotenv()

# import streamlit as st
# from langchain_google_genai import ChatGoogleGenerativeAI

# # model
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# # title & description
# st.title("Python AI Chatbot")
# st.markdown("Ask me anything about Python programming")

# # sidebar
# st.sidebar.title("About")
# st.sidebar.write("This is a Python teacher chatbot built with Streamlit and Gemini")

# # clear chat button
# if st.sidebar.button("Clear Chat"):
#     st.session_state.messages = []

# # session state
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # display old messages
# for message in st.session_state.messages:
#     st.chat_message(message["role"]).markdown(message["content"])

# # input
# query = st.chat_input("Ask Python question...")

# if query:
#     # show user message
#     st.chat_message("user").markdown(query)
#     st.session_state.messages.append({"ro le": "user", "content": query})

#     # system prompt
#     prompt = "You are a helpful Python teacher. " + query

#     # loading spinner
#     with st.spinner("Thinking..."):
#         res = llm.invoke(prompt)

#     # show AI response
#     st.chat_message("ai").markdown(res.content)
#     st.session_state.messages.append({"role": "ai", "content": res.content})