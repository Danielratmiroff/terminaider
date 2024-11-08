import sys
import re
import logging
from typing import Optional
import uuid
from src.agent import call_model
from src.ai_interface import get_ai_interface
from src.prompts import PROMPT_TEMPLATE, SYSTEM_PROMPT
import pyperclip
import markdown
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, START, END


def run_chat(
        init_prompt: Optional[str],
        interface: str
):
    # Define a new graph
    builder = StateGraph(state_schema=MessagesState)

    # Define the two nodes we will cycle between
    builder.add_edge(START, "model")
    builder.add_node("model", call_model)

    graph = builder.compile()

    session_id = uuid.uuid4()
    llm = get_ai_interface(interface=interface)
    config = {
        "configurable": {
            "session_id": session_id,
            "llm_interface": llm
        }
    }

    try:
        # print("** Welcome to the AI Chat Interface!")
        system_message = SystemMessage(content="Welcome to the AI Chat Interface!")

        while True:
            user_input = input("Enter your prompt: ")
            if user_input.lower() == "exit":
                break

            input_message = HumanMessage(content=user_input)

            for event in graph.stream({"messages": [input_message]}, config, stream_mode="values"):
                event["messages"][-1].pretty_print()

    except Exception as e:
        print(f"Error reading input: {e}")
