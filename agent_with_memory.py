# search on langchain-docs core components, there is topic of short term memory, read, memory is part of langgraph, we use checkpointer, install langgraph

from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_grok import ChatGrok
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

llm=ChatGrok(model="openai/gpt-oss-20b")
search = GoogleSerperAPIWrapper()

# search.run("Address of Ufone")
agent=create_agent(
    model=llm,
    tools=[search.run],
    system_prompt="you are an agent and can search for any question on google.",
    checkpointer=MemorySaver()
    
)
question="Who won women's world cup 2025"
response=agent.invoke({"messages":[{"role":"user", "content":question}]},
                      {"configurable":{"thread_id":1}})
response["messages"]
