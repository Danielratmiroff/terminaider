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

# logging.basicConfig(level=logging.INFO)


chats_by_session_id = {}


def get_chat_history(session_id: str) -> InMemoryChatMessageHistory:
    chat_history = chats_by_session_id.get(session_id)
    if chat_history is None:
        chat_history = InMemoryChatMessageHistory()
        chats_by_session_id[session_id] = chat_history
    return chat_history


# Define a new graph
# builder = StateGraph(state_schema=MessagesState)

# llm = get_ai_interface("huggingface")
# llm = HuggingFaceEndpoint(
#     repo_id="microsoft/Phi-3-mini-4k-instruct",
#     task="text-generation",
#     max_new_tokens=512,
#     do_sample=False,
#     repetition_penalty=1.03,
# )

# logging.info(f"Using interface: {llm}")
# tools = [search]
# tool_node = ToolNode(tools)
# model = ChatHuggingFace(llm=llm)
# bound_model = model.bind_tools(tools)

class AnalysisResult(TypedDict):
    messages: List[BaseMessage]
    code_analysis: str


@dataclass(frozen=True)
class MessagesState(TypedDict):
    messages: List[BaseMessage]
    code_analysis: str

# Define the function that calls the model


def call_model(state: MessagesState, config: RunnableConfig) -> AnalysisResult:
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


# # Define the two nodes we will cycle between
# builder.add_edge(START, "model")
# builder.add_node("model", call_model)

# graph = builder.compile()

# # Here, we'll create a unique session ID to identify the conversation
# session_id = uuid.uuid4()
# config = {"configurable": {"session_id": session_id}}

# input_message = HumanMessage(content="hi! I'm bob")
# for event in graph.stream({"messages": [input_message]}, config, stream_mode="values"):
#     event["messages"][-1].pretty_print()

# # Here, let's confirm that the AI remembers our name!
# input_message = HumanMessage(content="what was my name?")
# for event in graph.stream({"messages": [input_message]}, config, stream_mode="values"):
#     event["messages"][-1].pretty_print()
