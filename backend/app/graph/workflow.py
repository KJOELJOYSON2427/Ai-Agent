from langgraph.graph import StateGraph, START, END

from app.state.state import AgentState

from app.agents.orchestrator import orchestrator_agent
from app.agents.requirements_review import requirements_review_agent

from app.agents.requirements import requirements_agent
from app.agents.architecture import architecture_agent
from app.graph.router import  route_from_orchestrator,route_after_requirements_review
builder = StateGraph(AgentState)


builder.add_node(
    "orchestrator",
    orchestrator_agent
)

builder.add_node(
    "requirements_agent",
    requirements_agent
)
builder.add_node("requirements_review", requirements_review_agent)

builder.add_node(
    "architecture_agent",
    architecture_agent
)




# START → Orchestrator
builder.add_edge(START, "orchestrator")


# Orchestrator → Requirements Agent
builder.add_conditional_edges(
    "orchestrator",
    route_from_orchestrator,
    {
        "requirements_agent": "requirements_agent"
    }
)


# Requirements Agent → Requirements Review
builder.add_edge(
    "requirements_agent",
    "requirements_review"
)
# Requirements Review → Architecture OR Requirements Revision
builder.add_conditional_edges(
    "requirements_review",
    route_after_requirements_review,
    {
        "architecture_agent": "architecture_agent",
        "requirements_revision": "requirements_agent"
    }
)

builder.add_edge(
    "architecture_agent",
    END
)

graph = builder.compile()