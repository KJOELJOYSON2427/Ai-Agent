from langgraph.graph import StateGraph, START, END

from app.state.state import AgentState

from app.agents.orchestrator import orchestrator_agent
from app.agents.requirements import requirements_agent
from app.agents.architecture import architecture_agent

builder = StateGraph(AgentState)


builder.add_node(
    "orchestrator",
    orchestrator_agent
)

builder.add_node(
    "requirements_agent",
    requirements_agent
)
builder.add_node(
    "architecture_agent",
    architecture_agent
)

builder.add_edge(
    START,
    "orchestrator"
)


def route_from_orchestrator(state: AgentState):

    return state["next_step"]


builder.add_conditional_edges(
    "orchestrator",
    route_from_orchestrator,
    {
        "requirements_agent": "requirements_agent"
    }
)


builder.add_edge(
    "requirements_agent",
    "architecture_agent"
)

builder.add_edge(
    "architecture_agent",
    END
)

graph = builder.compile()