import os
import importlib
import streamlit as st
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
import json
import logging
logging.basicConfig(level=logging.INFO)

JINA_API_KEY = st.secrets["JINA_API_KEY"]
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

import utils
importlib.reload(utils)
from utils import *

# load_dotenv()

# Initialize model
model = ChatOpenAI(model_name="gpt-4o", temperature=0, api_key=OPENAI_API_KEY)

# Define schema
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Tool
search = GoogleSerperAPIWrapper(k=2, api_key=SERPER_API_KEY)

@tool
def google_search(query: str) -> str:
    """Conduct Search on Wake Forest MSBA Website for user question"""
    google_results = search.results(f'{query} site:business.wfu.edu/',)
    
    if not google_results:
        return "No results found for your query."
    
    documents = ggsearch_reformat(google_results)
    link = documents[0].metadata['source']
    title = documents[0].metadata['title']
    jina_content = jina_scrape(link)
    documents.append(Document(page_content=jina_content, metadata={'source': link, 'title': title}))
    return documents

tools = [google_search]

# Bind the tool with gpt-4o
model_with_tools = model.bind_tools(tools)

# Define the tool node
tools_by_name = {tool.name: tool for tool in tools}

def serialize_tool_result(tool_result):
    if isinstance(tool_result, list) and all(isinstance(doc, Document) for doc in tool_result):
        return [
            {
                "metadata": doc.metadata,
                "page_content": doc.page_content
            } for doc in tool_result
        ]
    return str(tool_result)

def tool_node(state: State):
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        try:
            tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        except Exception as e:
            tool_result = f"Error while invoking tool: {str(e)}"
        
        tool_result_serialized = serialize_tool_result(tool_result)
        
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result_serialized),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}


SYSTEM_PROMPT = SystemMessage(
    """You are a helpful AI assistant. You get access to Wake Forest School of Business tools to explore website information. 
    If users ask questions about the Wake Forest School of Business, use the tool to collect more information."""
)

# Define the node that calls the model
def call_model(state: State, config: RunnableConfig):

    formatted_messages = [
        {"role": msg[0], "content": msg[1]} if isinstance(msg, tuple) else msg
        for msg in state['messages']
    ]
    response = model_with_tools.invoke([SYSTEM_PROMPT] + formatted_messages, config)
    return {'messages': [response]}

# Define a conditional edge whether we should continue to use the tool or end
def should_continue(state: State):
    if not state['messages'][-1].tool_calls:
        return "end"
    else:
        return "continue"

# Define and compile the graph

def main():
    st.title("Wake Forest Business School Q/A")
    
    # Example questions for user guidance
    examples = [
        "What are the application requirements for the MSBA program?",
        "What is the curriculum for the MSBA program like?",
        "Can you provide information on career services?",
        "How does Wake Forest support international students?"
    ]

        # Use an expander to organize the examples
    with st.expander("Examples of questions you can ask:"):
        for idx, example in enumerate(examples):
            if st.button(example, key=f"example_button_{idx}"):
                st.session_state.user_input = example

    # Initialize session state for SQLite connection and memory
    if 'conn' not in st.session_state:
        st.session_state.conn = sqlite3.connect(":memory:", check_same_thread=False)
        st.session_state.memory = SqliteSaver(st.session_state.conn)

    # Ensure 'user_input' is initialized in session state
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''

    # Create a form to handle both Enter key and Submit button
    with st.form(key='my_form'):
        user_input = st.text_input(
            "Tell us what program or information you are curious about:",
            value=st.session_state.user_input
        )
        submit_button = st.form_submit_button(label='Submit')
        
    if submit_button and user_input:
        with st.spinner('Processing your request...'):
            # Define and compile the graph
            workflow = StateGraph(State)
            workflow.add_node('agent', call_model)
            workflow.add_node('tools', tool_node)
            workflow.add_edge(START, 'agent')
            workflow.add_conditional_edges('agent', should_continue, {'continue': 'tools', 'end': END})
            workflow.add_edge('tools', 'agent')
            compiled_graph = workflow.compile(checkpointer=st.session_state.memory)
            
            # Example usage
            config = {'configurable': {'thread_id': '2'}}
            inputs = {"messages": user_input}
            messages = compiled_graph.invoke(inputs, config)

        # Display the response
        for m in [messages['messages'][-1]]:
            st.write(m.content)
    
    # Add a footer note
    st.markdown("---")
    st.caption("Nam Tran, MSBA '24")
if __name__ == "__main__":
    main()