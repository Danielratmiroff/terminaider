import os
from groq import Groq
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
console = Console()


DEFAULT_PROMPT = """
    Act as an expert software developer. Always use best practices when coding. 
    Be very concise, keep your responses straight to the point and be very clear in your responses.
    Ommit any unnecessary information and prerequisites.
    You *MUST* use markdown and pay close attention to the formatting to make your response as clear as possible.
      """

def get_groq_response(prompt):
    client = Groq(
        api_key=os.environ.get('GROQ_API_KEY'),
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': DEFAULT_PROMPT + prompt
            }
        ],
        model='llama3-70b-8192',
    )

    return chat_completion.choices[0].message.content


def main():
    chr_num = 70

    console.print(Panel(Text("Welcome to the AI Chat Interface!", style="bold magenta"), expand=False))
    console.print("\n" + "="*chr_num + "\n", style="bold green")

    while True:
        user_input = Prompt.ask("[bold blue]Enter your prompt[/bold blue]")
        if user_input.lower() == 'exit':
            break

        response = get_groq_response(user_input)
        markdown_response = Markdown(response)
        console.print("\n" + "-"*chr_num + "\n", style="bold yellow")
        console.print(markdown_response)
        console.print("\n" + "-"*chr_num + "\n", style="bold yellow")

if __name__ == "__main__":
    main()