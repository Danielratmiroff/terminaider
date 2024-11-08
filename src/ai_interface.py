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


class GroqModel(BaseModel):
    name: str = "llama-3.2-90b-text-preview"
    temperature: float = 0.7
    max_tokens: int = 1024


class HuggingFaceModel(BaseModel):
    name: str = "Qwen/Qwen2.5-72B-Instruct"
    temperature: float = 0.7
    max_tokens: int = 32760


class OpenAIModel(BaseModel):
    name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4096


def get_ai_interface(interface: str):
    """
    Get the interface to use for the AI chat.
    """
    logging.info(f"Using interface: {interface} {Interfaces.__members__}")

    match interface:
        case Interfaces.OPENAI:
            api_key = get_openai_api_key()
            model = OpenAIModel()

            return ChatOpenAI(
                model_name=model.name,
                temperature=model.temperature,
                openai_api_key=api_key,
            )

        case Interfaces.GROQ:
            api_key = get_groq_api_key()
            model = GroqModel()

            return ChatGroq(
                model=model.name,
                temperature=model.temperature,
                max_tokens=model.max_tokens,
                api_key=api_key
            )

        case _:
            # Default to HuggingFace if no match is found
            model = HuggingFaceModel()
            api_key = get_api_huggingface_key()

            return ChatHuggingFace(
                llm=HuggingFaceEndpoint(
                    repo_id=model.name,
                    task="text-generation",
                    max_new_tokens=128,
                    temperature=0.5,
                    huggingfacehub_api_token=api_key,
                    repetition_penalty=1.03,
                )
            )
