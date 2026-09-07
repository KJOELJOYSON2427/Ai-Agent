import os
from typing import Literal

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from pydantic import BaseModel

from app.state.state import AgentState

from dotenv import load_dotenv
from app.state.state import AgentState


class RequirementsDecision(BaseModel):
    requirements: str
    next_step: Literal[
        "architecture_agent",
        "requirements_revision"
    ]
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")

)
structured_llm = llm.with_structured_output(
    RequirementsDecision
)
# def requirements_agent(state: AgentState):

#     system_message = SystemMessage(
#         content="""
# You are a Requirements Analyst Agent.

# Convert the user's software idea into structured
# software requirements.

# Produce:

# 1. Project Goal
# 2. Stakeholders
# 3. User Roles
# 4. Functional Requirements
# 5. Non-Functional Requirements
# 6. Business Rules
# 7. Assumptions

# Do NOT design the architecture.
# Do NOT write code.
# Do NOT choose technologies.
# """
#     )

#     human_message = HumanMessage(
#         content=state["requirement"]
#     )

#     response = llm.invoke([
#         system_message,
#         human_message
#     ])

#     return {
#         "requirements": response.content,
#         "messages": [
#             response
#         ]
#     }

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)



def requirements_agent(state: AgentState):

    system_message = SystemMessage(
        content="""
You are a Requirements Analyst Agent.

Convert the user's software idea into structured
software requirements.

Produce:

1. Project Goal
2. Stakeholders
3. User Roles
4. Functional Requirements
5. Non-Functional Requirements
6. Business Rules
7. Assumptions

Do NOT design the architecture.
Do NOT write code.
Do NOT choose technologies.
"""
    )

    human_message = HumanMessage(
        content=state["requirement"]
    )

    response = structured_llm.invoke([
        system_message,
        human_message
    ])

    return {
        "requirements": response.requirements,

        "next_step": response.next_step,

        "messages": [
            AIMessage(content=response.requirements)
        ]
    }