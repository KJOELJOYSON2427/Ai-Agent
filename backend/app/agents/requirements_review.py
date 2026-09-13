from typing import Literal
from pydantic import BaseModel

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from langchain_google_genai import ChatGoogleGenerativeAI

from app.state.state import AgentState


class RequirementsReview(BaseModel):
    decision: Literal[
        "architecture_agent",
        "requirements_revision"
    ]
    feedback: str


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)

structured_llm = llm.with_structured_output(
    RequirementsReview
)


def requirements_review_agent(state: AgentState):

    system_message = SystemMessage(
        content="""
You are a Requirements Review Agent.

Review the requirements produced by the
Requirements Analyst.

Check for:

1. Completeness
2. Clarity
3. Ambiguous requirements
4. Missing functional requirements
5. Missing non-functional requirements
6. Conflicting requirements
7. Missing business rules

If the requirements are sufficiently complete and clear,
choose architecture_agent.

If important information is missing or unclear,
choose requirements_revision.

Provide concise feedback explaining your decision.
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
        "next_step": response.decision,
        "review_feedback": response.feedback,

        "messages": [
            AIMessage(content=response.feedback)
        ]
    }