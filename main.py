
import logging
from typing import List
from pydantic import BaseModel
import typer
from src import get_app_name, run_chat, get_package_version

# logging.basicConfig(level=logging.DEBUG)

app = typer.Typer()


class Config(BaseModel):
    prompt_type: str


@app.command()
def termi(
    prompt: str = typer.Argument(None),
    # TODO: make the ai itself determine if it should run or not
    # run: bool = typer.Option(
    #     False,
    #     "-r",
    #     "--run",
    #     help="Execute the prompt"
    # ),
    interface: str = typer.Option(
        "groq",
        "-i",
        "--interface",
        help="Interface to use for the AI chat, e.g. groq, openai",
    ),
    version: bool = typer.Option(
        False,
        "-v",
        "--version",
        help="Show the version of the application")
):
    """
    Command Line Interface (CLI) command for interacting with the AI chat interface.

    Parameters:
    - prompt: A list of strings representing the prompt to be processed by the AI.
    - run: A boolean flag to execute the prompt if set to True.
    - version: A boolean flag to display the current version of the application if set to True.
    """

    if version:
        print(f"v{get_package_version(get_app_name())}")
        raise typer.Exit()

    run_chat(
        init_prompt=prompt,
        interface=interface
    )


if __name__ == "__main__":
    app()
