"""
Dialog Roles library (Minimal)

This module defines a minimal set of functions and prompt for conversation flow with two participants:
1) A Wikipedia editor – asks questions based on their assigned role.
2) A domain expert – uses a search engine to answer as accurately as possible.

The actual chain or LLM calls (e.g. generate_question) can be implemented outside this file,
using these helpers.
"""

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

try:
    from Promt import Dialog_Roles_Promt
except ImportError:
    Dialog_Roles_Promt = "You are a Wikipedia editor with a specific persona. Ask relevant questions."

# InterviewState: dict เก็บ state สนทนา (messages, editor, references ฯลฯ)
try:
    from Interview_State import InterviewState
except ImportError:
    pass  # หรือกำหนด mock/fallback ได้ตามต้องการ


"""
Dialog Roles library

This module defines a conversation flow with two participants:
1) A Wikipedia editor (generate_question) – asks questions based on their assigned role.
2) A domain expert (gen_answer_chain) – uses a search engine to answer as accurately as possible.

The generate_question function transforms the conversation state so that the Wikipedia editor
asks questions about the topic. The conversation is stored in InterviewState.
"""


from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import MessagesPlaceholder
from Promt_Quant  import *
from Interview_State import InterviewState

from langchain_core.prompts import ChatPromptTemplate



gen_qn_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",Dialog_Roles_Promt
           ,
        ),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)


def tag_with_name(ai_message: AIMessage, name: str):
    ai_message.name = name
    return ai_message


def swap_roles(state: InterviewState, name: str):
    converted = []
    for message in state["messages"]:
        if isinstance(message, AIMessage) and message.name != name:
            message = HumanMessage(**message.model_dump(exclude={"type"}))
        converted.append(message)
    return {"messages": converted}