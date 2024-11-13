import sys
import pyperclip
import re
import logging
from typing import Callable, List, Optional, Tuple
import uuid
from terminaider.themes.themes import CATPUCCINO_MOCCA
from terminaider.agent import call_model
from terminaider.ai_interface import get_ai_interface
from terminaider.utils import clean_code_block, print_token_usage
from terminaider.prompts import SYSTEM_PROMPT
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

# logging.basicConfig(level=logging.DEBUG)


def initialize_chat(first_call: bool, input_message: HumanMessage) -> MessagesState:
    if first_call:
        messages = [SYSTEM_PROMPT, input_message]
    else:
        messages = [input_message]

    return MessagesState(
        messages=messages,
        code_analysis=""
    )


def handle_code_summary(code_summary: str, console: Console) -> None:
    """
    Display and copy the code analysis summary.
    """
    console.print(Markdown("\n## Code Summary:"))
    console.print(Markdown(code_summary))

    # Copy the code analysis to the clipboard
    logging.debug(f"\nCopying code analysis to clipboard.\n{clean_code_block(code_summary)}")
    pyperclip.copy(clean_code_block(code_summary))
    print("Code analysis copied to clipboard. ✅")


def run_chat(
        init_prompt: Optional[str],
        interface: str
):
    console = Console(theme=CATPUCCINO_MOCCA, highlight=True)
    is_first_call = True

    # Define a new graph
    builder = StateGraph(state_schema=MessagesState)

    # Define the two nodes we will cycle between
    builder.add_edge(START, "model")
    builder.add_node("model", call_model)

    # Compile the graph
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
        while True:
            if init_prompt and is_first_call:
                input_message = HumanMessage(content=init_prompt)
                chat_state = initialize_chat(is_first_call, input_message)

            else:
                user_input = input("✨ Message AI:\n> ")
                if user_input.lower() == "exit":
                    console.print("Exiting... auf Wiedersehen! 👋")
                    break

                input_message = HumanMessage(content=user_input)
                chat_state = initialize_chat(is_first_call, input_message)

            # Stream the messages through the graph
            for event in graph.stream(chat_state, config, stream_mode="values"):
                # Skip the first event
                if is_first_call:
                    is_first_call = False
                    continue

                logging.debug(f"Stream Event: {event}")

                latest_message = event["messages"][-1]
                messages_context = latest_message.content
                markdown_messages = Markdown(messages_context)
                console.print(markdown_messages)

                code_analysis = event.get("code_analysis")
                if code_analysis and event["code_analysis"] != "None":
                    handle_code_summary(event["code_analysis"], console)

    except KeyboardInterrupt:
        console.print("\nTschuss! 👋")
    except Exception as e:
        print(f"Error reading input: {e}")
