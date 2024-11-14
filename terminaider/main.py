
import logging
from typing import Annotated, List, Optional
from pydantic import BaseModel
import typer
from terminaider import get_app_name, run_chat, get_package_version
from terminaider.ai_interface import Interfaces
from terminaider.config import ConfigManager

# logging.basicConfig(level=logging.DEBUG)

app = typer.Typer()


def interface_callback(value: str) -> Interfaces:
    """Validate and convert interface input"""
    try:
        return Interfaces(value.lower())
    except ValueError:
        valid_interfaces = ", ".join([i.value for i in Interfaces])
        raise typer.BadParameter(f"Invalid interface. Must be one of: {valid_interfaces}")


@app.command()
def termi(
    prompt: Annotated[Optional[str],
                      typer.Argument(
                          help="The prompt to be processed by the AI chat.")] = None,
    interface: Annotated[str,
                         typer.Option(
                             "--interface",
                             "-i",
                             callback=interface_callback,
                             help="Interface to use for the AI chat, e.g. groq, openai"
                         )] = Interfaces.GROQ.value,
    version: Annotated[bool,
                       typer.Option(
                           "--version",
                           "-v",
                           help="Show the version of the application",
                           is_eager=True
                       )] = False,
):
    """
    Command Line Interface (CLI) command for interacting with the AI chat interface.

    Parameters:
    - prompt: A list of strings representing the prompt to be processed by the AI.
    - run: A boolean flag to execute the prompt if set to True.
    - version: A boolean flag to display the current version of the application if set to True.
    """
    configManager = ConfigManager(get_app_name())

    logging.debug(f"Parameters: prompt={prompt}, interface={interface}, version={version}")

    if interface and configManager.get_config('interface') != interface:
        configManager.update_config('interface', interface.value)

    if version:
        print(f"v{get_package_version(get_app_name())}")
        raise typer.Exit()

    run_chat(
        init_prompt=prompt,
        interface=interface
    )


def run():
    """Entry point for the application"""
    app()


if __name__ == "__main__":
    run()
