from enum import Enum
import logging
from typing import Dict
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

from src.utils import get_api_huggingface_key, get_groq_api_key, get_openai_api_key


class Interfaces(Enum):
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"
    GROQ = "groq"


class AIModel(BaseModel):
    llm: str
    temperature: float
    max_tokens: int


groq_model = AIModel(
    llm="llama-3.2-90b-text-preview",
    temperature=0.7,
    max_tokens=5000
)

huggingface_model = AIModel(
    llm="Qwen/Qwen2.5-72B-Instruct",
    temperature=1,
    # max_tokens=32760
    max_tokens=2048
)

openai_model = AIModel(
    llm="gpt-4",
    temperature=0.7,
    # max_tokens=4096
    max_tokens=5000
)


def get_ai_interface(
        interface: str,
        advanced: bool = True
):
    """
    Get the interface to use for the AI chat.
    """

    match interface:
        case Interfaces.OPENAI:
            api_key = get_openai_api_key()
            logging.info(f"Using OpenAI Interface with API Key: {api_key}")

            return ChatOpenAI(
                model_name=openai_model.llm,
                temperature=openai_model.temperature,
                openai_api_key=api_key,
                max_tokens=openai_model.max_tokens
            )

        case Interfaces.GROQ:
            api_key = get_groq_api_key()
            logging.info(f"Using GROQ Interface with API Key: {api_key}")

            return ChatGroq(
                model=groq_model.llm,
                temperature=groq_model.temperature,
                max_tokens=groq_model.max_tokens,
                api_key=api_key
            )

        case _:
            # Default to HuggingFace if no match is found
            api_key = get_api_huggingface_key()
            logging.info(f"Using HuggingFace Interface with API Key: {api_key}")

            return ChatHuggingFace(
                llm=HuggingFaceEndpoint(
                    repo_id=huggingface_model.llm,
                    task="text-generation",
                    max_new_tokens=huggingface_model.max_tokens,
                    temperature=huggingface_model.temperature,
                    huggingfacehub_api_token=api_key,
                    repetition_penalty=1.03,
                )
                # ChatHuggingFace discards the max_new_tokens parameter for invocations
                # We need to pass it as a bind_tools parameter
                # https://github.com/langchain-ai/langchain/issues/25219
            ).bind_tools(tools=[], max_tokens=huggingface_model.max_tokens)
