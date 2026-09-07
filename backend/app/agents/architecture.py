import os

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import SystemMessage, HumanMessage

from app.state.state import AgentState
from dotenv import load_dotenv

from typing import Literal
from pydantic import BaseModel
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
)
class ArchitectureDecision(BaseModel):
    architecture: str
    next_step: Literal[
        "database_agent",
        "architecture_revision"
    ]


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")

)
structured_llm = llm.with_structured_output(
    ArchitectureDecision
)


# def architecture_agent(state: AgentState):

#     system_message = SystemMessage(
#         content="""
# You are an Architecture Agent.

# Design the software architecture based on the
# requirements provided by the Requirements Agent.

# Produce:

# 1. Architecture style
# 2. Major components
# 3. Responsibilities of each component
# 4. Communication between components
# 5. Main data flow
# 6. Scalability considerations
# 7. Security considerations

# Do NOT write code.
# Do NOT implement the database schema.
# Do NOT produce detailed API code.
# """
#     )

#     human_message = HumanMessage(
#         content=state["requirements"]
#     )

#     response = llm.invoke([
#         system_message,
#         human_message
#     ])

#     return {
#         "architecture": response.content,
#         "messages": [
#             response
#         ]
#     }

def architecture_agent(state: AgentState):

    system_message = SystemMessage(
        content="""
        You are an Architecture Agent.

Design the software architecture based on the
requirements provided by the Requirements Agent.

Produce:

1. Architecture style
2. Major components
3. Responsibilities of each component
4. Communication between components
5. Main data flow
6. Scalability considerations
7. Security considerations

Do NOT write code.
Do NOT implement the database schema.
Do NOT produce detailed API code.


After creating the architecture, decide what should happen next.

Choose:

- database_agent
    if the architecture is sufficiently complete.

- architecture_revision
    if the architecture needs further refinement.

Return the architecture and your decision.
"""
    )

    human_message = HumanMessage(
        content=state["requirements"]
    )

    response = structured_llm.invoke([
        system_message,
        human_message
    ])

    return {
    "architecture": response.architecture,
    "next_step": response.next_step,
    "messages": [
        AIMessage(content=response.architecture)
    ]
}