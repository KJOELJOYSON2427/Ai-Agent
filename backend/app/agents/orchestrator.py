import os
from typing import Literal

from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.state.state import AgentState
from dotenv import load_dotenv

load_dotenv()


class OrchestratorDecision(BaseModel):
    next_step: Literal[
        "requirements_agent",
        "architecture_agent",
        "database_agent",
        "coding_agent",
        "testing_agent",
        "review_agent",
        "documentation_agent",
    ]


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

structured_llm = llm.with_structured_output(
    OrchestratorDecision
)


def orchestrator_agent(state: AgentState):

    system_message = SystemMessage(
        content="""
You are the Orchestrator Agent of a software engineering system.

Analyze the user's software requirement.

Choose the appropriate next agent.

Available agents:

- requirements_agent
- architecture_agent
- database_agent
- coding_agent
- testing_agent
- review_agent
- documentation_agent

For the current stage of the system, always choose:

requirements_agent
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
        "next_step": response.next_step
    }