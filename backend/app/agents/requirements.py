import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage

from app.state.state import AgentState

from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")

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

    response = llm.invoke([
        system_message,
        human_message
    ])

    return {
        "requirements": response.content,
        "messages": [
            response
        ]
    }
