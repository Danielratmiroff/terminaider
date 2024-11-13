from rich.syntax import Syntax
from rich.theme import Theme
from rich.markdown import Markdown
from rich.console import Console
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
import markdown
import pyperclip
from terminaider.prompts import SYSTEM_PROMPT
from terminaider.utils import clean_code_block, print_token_usage, sum_tokens
from terminaider.ai_interface import get_ai_interface
from terminaider.agent import UsageMetadata, call_model
from terminaider.themes.themes import CATPUCCINO_MOCCA
import uuid
from typing import Callable, List, Optional, Tuple
import logging
import re
import sys
pyperclip


def initialize_chat(first_call: bool, input_message: HumanMessage) -> MessagesState:
    if first_call:
        messages = [SYSTEM_PROMPT, input_message]
    else:
        messages = [input_message]

    return MessagesState(
        messages=messages,
        code_analysis="",
        usage_metadata=UsageMetadata(
            input_tokens=0,
            output_tokens=0,
            total_tokens=0
        ))


def handle_code_summary(code_summary: str, console: Console) -> None:
    """
    Display and copy the code analysis summary.
    """
    console.print(Markdown("\n## Code Summary:"))
    console.print(Markdown(code_summary))

    # Copy the code analysis to the clipboard
    logging.debug(f"\nCopying code analysis to clipboard.\n{clean_code_block(code_summary)}")
    pyperclip.copy(clean_code_block(code_summary))
    print("Code summary copied to clipboard. ✅")


def initialize_state_graph():
    # Define a new graph
    builder = StateGraph(state_schema=MessagesState)

    # Define the two nodes we will cycle between
    builder.add_edge(START, "model")
    builder.add_node("model", call_model)

    # Compile the graph
    graph = builder.compile()

    return graph


def run_chat(
        init_prompt: Optional[str],
        interface: str
):
    total_token_usage = UsageMetadata(input_tokens=0, output_tokens=0, total_tokens=0)
    console = Console(theme=CATPUCCINO_MOCCA, highlight=True)
    is_first_call = True
    session_id = uuid.uuid4()

    state_graph = initialize_state_graph()
    llm = get_ai_interface(interface=interface)

    config = {
        "configurable": {
            "session_id": session_id,
            "llm_interface": llm
        }
    }

    try:
        while True:
            if init_prompt and is_first_call:
                input_message = HumanMessage(content=init_prompt)
                chat_state = initialize_chat(is_first_call, input_message)

            else:
                user_input = input("\n✨ Message AI:\n> ")
                if user_input.lower() == "exit":
                    print_token_usage(total_token_usage, console=console)
                    console.print("Exiting... auf Wiedersehen! 👋")
                    break

                input_message = HumanMessage(content=user_input)
                chat_state = initialize_chat(is_first_call, input_message)

            is_first_call = False

            # Stream the messages through the graph
            for event in state_graph.stream(chat_state, config, stream_mode="values"):
                logging.debug(f"Stream Event: {event}")
                # print(f"event: {event}")

                latest_message = event["messages"][-1]

                # Only process AI messages
                if isinstance(latest_message, AIMessage):
                    # Display AI message content
                    console.print(Markdown(latest_message.content))

                    # Process code analysis summary if available
                    code_analysis = event.get("code_analysis")
                    if code_analysis and code_analysis != "None":
                        handle_code_summary(code_analysis, console)

                    # Update total token usage
                    current_token_usage = event.get("usage_metadata")
                    if current_token_usage:
                        total_token_usage = sum_tokens(total_token_usage, current_token_usage)

    except KeyboardInterrupt:
        print_token_usage(total_token_usage, console=console)
        console.print("\nTschuss! 👋")
    except Exception as e:
        print(f"Error reading input: {e}")
