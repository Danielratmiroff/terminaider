from dataclasses import dataclass
import logging
from typing import List, Literal, TypedDict
import uuid

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, MessagesState, StateGraph


chats_by_session_id = {}


def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    chat_history = chats_by_session_id.get(session_id)
    if chat_history is None:
        chat_history = InMemoryChatMessageHistory()
        chats_by_session_id[session_id] = chat_history
    return chat_history


@dataclass(frozen=True)
class MessagesState(TypedDict):
    messages: List[BaseMessage]
    code_analysis: str

# Define the function that calls the model


def call_model(state: MessagesState, config: RunnableConfig) -> MessagesState:
    # Make sure that config is populated with the session id
    logging.info(f"Config: {config}")
    if "configurable" not in config or "session_id" not in config["configurable"] or "llm_interface" not in config["configurable"]:
        raise ValueError(
            "Make sure that the config includes the following information: {'configurable': {'session_id': 'some_value'}, {'llm_interface': 'some_interface'}"
        )

    # Fetch the history of messages and append to it any new messages.
    chat_history = get_chat_history(config["configurable"]["session_id"])
    llm = config["configurable"]["llm_interface"]

    messages = list(chat_history.messages) + state["messages"]
    response = llm.invoke(messages)
    logging.info(f"\nAI Response: {response}")

    main_response, code_analysis = extract_response_parts(response.content)

    # Create a new message with the response content
    ai_message = type(response)(content=main_response)

    # Update the chat message history to include
    chat_history.add_messages(state["messages"] + [ai_message])

    return {
        "messages": [ai_message],
        "code_analysis": code_analysis
    }


def extract_response_parts(response_content: str) -> tuple:
    """
    Helper function to split the response into main content and code analysis.

    Parameters:
    - response_content: The content of the response to be split.

    Returns:
    - A tuple containing the main response and code analysis.
    """
    content_parts = response_content.split("[CODE_ANALYSIS]")
    main_response = content_parts[0].strip()
    logging.info(f"Main response: {main_response}")
    code_analysis = content_parts[1].strip() if len(content_parts) > 1 else "None"
    logging.info(f"Code analysis: {code_analysis}")
    return (main_response, code_analysis)
