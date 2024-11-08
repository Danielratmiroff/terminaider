from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage


EXECUTE_PROMPT = PromptTemplate(
    input_variables=[],
    template="""
    Please provide the single best code solution for the following request.
    Carefully consider multiple options and choose the most optimal one. 
    Wrap **ONLY** the code snippet suggested within **<code>** markdown format.

    Note: Ensure your response is concise, well-formatted using MARKDOWN, and adheres to best
    practices in software development.
    """
)

DEFAULT_PROMPT = PromptTemplate(
    input_variables=[],
    template="""
    Act as an expert software developer. Always use best practices when coding. 
    Be very concise, keep your responses straight to the point and be very clear in your responses.
    Omit any unnecessary information and prerequisites.
    You *MUST* use markdown and pay close attention to the formatting to make your response as clear as possible.
    """
)

SYSTEM_PROMPT = SystemMessage(
    content="""
    Act as an expert software developer. Always use best practices when coding.
    Be very concise, keep your responses straight to the point and be very clear in your responses.
    Omit any unnecessary information and prerequisites.
    You *MUST* use markdown and pay close attention to the formatting to make your response as clear as possible.
    """
)


PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    SystemMessage(
        content="""
        Act as an expert software developer. Always use best practices when coding.
        Be very concise, keep your responses straight to the point and be very clear in your responses.
        Omit any unnecessary information and prerequisites.
        You *MUST* use markdown and pay close attention to the formatting to make your response as clear as possible.
    """
    ),
    MessagesPlaceholder(
        "input"
    )
])

# CHAT_PTOMP = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             """
#             Act as an expert software developer. Always use best practices when coding.
#             Be very concise, keep your responses straight to the point and be very clear in your responses.
#             Omit any unnecessary information and prerequisites.
#             You *MUST* use markdown and pay close attention to the formatting to make your response as clear as possible.
#             """
#         ),
#         (
#             "user",
#             "{input}"
#         )
#     ]
# )