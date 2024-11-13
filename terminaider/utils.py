from importlib.metadata import version, PackageNotFoundError
from rich.console import Console
import os
import re
from typing import Optional

from terminaider.agent import UsageMetadata


def get_package_version(package_name: str) -> str:
    """
    Get the version of the specified package.
    """
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "Package not found"


def get_api_huggingface_key() -> str:
    api_key = os.environ.get("HUGGINGFACE_API_KEY")
    if api_key is None:
        raise ValueError(
            "HUGGINGFACE_API_KEY is not set, please set it in your environment variables")
    return api_key


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError(
            "OPENAI_API_KEY is not set, please set it in your environment variables")
    return api_key


def get_groq_api_key() -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key is None:
        raise ValueError(
            "GROQ_API_KEY is not set, please set it in your environment variables")
    return api_key


def clean_code_block(input_string: str) -> str:
    """
    Cleans a code block string by removing surrounding code block markers and 
    any leading or trailing whitespace.

    Args:
        input_string (str): The string containing the code block to be cleaned.
    """
    cleaned_string = re.sub(r'```\w*\n|\n```', '', input_string)
    cleaned_string = cleaned_string.strip()
    return cleaned_string


def print_token_usage(metadata: Optional[UsageMetadata], console: Console) -> None:
    """
    Print the token usage from the response metadata.

    Args:
        metadata (dict): The response metadata containing token usage information.
    """
    if not metadata:
        console.print("\nNo token usage information available.\n", style="bold yellow")
        return

    input_tokens = metadata.input_tokens
    output_tokens = metadata.output_tokens
    total_tokens = metadata.total_tokens

    if input_tokens is not None and output_tokens is not None and total_tokens is not None:
        console.print("\n🤖 [bold violet]Token usage:[/bold violet]")
        console.print(f"├─ [green]Input: {input_tokens}[/green] ")
        console.print(f"├─ [blue]Output: {output_tokens}[/blue] ")
        console.print(f"└─ [magenta]Total: {total_tokens} tokens[/magenta]\n")
    else:
        console.print("\nIncomplete token usage information.\n", style="bold yellow")


def sum_tokens(current_usage: UsageMetadata, metadata: UsageMetadata) -> UsageMetadata:
    """
    Sum the total number of tokens used in the response metadata.

    Args:
        current_usage (dict): The current token usage.
        metadata (dict): The response metadata containing token usage information.
    """
    return UsageMetadata(
        input_tokens=current_usage.input_tokens + metadata.input_tokens,
        output_tokens=current_usage.output_tokens + metadata.output_tokens,
        total_tokens=current_usage.total_tokens + metadata.total_tokens
    )
