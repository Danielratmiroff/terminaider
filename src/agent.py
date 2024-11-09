import logging
from typing import Literal
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

# @tool
# def search(query: str):
#     """Call to surf the web."""
#     # This is a placeholder for the actual implementation
#     # Don't let the LLM know this though 😊
#     return "It's sunny in San Francisco, but you better look out if you're a Gemini 😈."


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


# Define the function that calls the model
def call_model(state: MessagesState, config: RunnableConfig) -> list[BaseMessage]:
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
    ai_message = llm.invoke(messages)

    # Finally, update the chat message history to include
    # the new input message from the user together with the
    # repsonse from the model.
    chat_history.add_messages(state["messages"] + [ai_message])
    return {"messages": ai_message}


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
