import sys
import re
import logging
from typing import Optional
import uuid
from themes.themes import CATPUCCINO_MOCCA
from src.agent import call_model
from src.ai_interface import get_ai_interface
from src.prompts import SYSTEM_PROMPT
import pyperclip
import markdown
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, START, END
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from rich.syntax import Syntax

# Initialize the console with the custom theme
console = Console(theme=CATPUCCINO_MOCCA, highlight=True)


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
    llm = get_ai_interface(interface=interface, advanced=True)
    # slm = get_ai_interface(interface=interface, advanced=False)
    config = {
        "configurable": {
            "session_id": session_id,
            "llm_interface": llm
        }
    }

    try:

        # Initialize the chat with the system message
        first_call = True

        while True:
            user_input = input("Enter your prompt: ")
            if user_input.lower() == "exit":
                break

            input_message = HumanMessage(content=user_input)

            if first_call:
                messages = [SYSTEM_PROMPT, input_message]
                first_call = False
            else:
                messages = [input_message]

            initial_state = {
                "messages": messages,
                "code_analysis": ""
            }

            # Stream the messages through the graph
            for event in graph.stream(initial_state, config, stream_mode="values"):
                print(event["messages"])
                messages = event["messages"][-1].content

                markdown_messages = Markdown(messages)
                console.print(markdown_messages)

                if event["code_analysis"] != "None":
                    print("\nCode Analysis:")
                    print(event["code_analysis"])

    except Exception as e:
        print(f"Error reading input: {e}")
