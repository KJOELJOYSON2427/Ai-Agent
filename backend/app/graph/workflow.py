from langgraph.graph import StateGraph, START, END
import sqlite3
from app.state.state import AgentState
from langgraph.checkpoint.sqlite import SqliteSaver

from app.agents.orchestrator import orchestrator_agent
from app.agents.requirements_review import requirements_review_agent

from app.agents.requirements import requirements_agent
from app.agents.architecture import architecture_agent
from app.graph.router import  route_after_human_review, route_from_orchestrator,route_after_requirements_review
from app.agents.human_review import human_review
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

builder.add_node("human_review", human_review)


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
        "architecture_agent": "human_review",
        "requirements_revision": "requirements_agent"
    }
)


builder.add_conditional_edges(
    "human_review",
    route_after_human_review,
    {
        "approve": "architecture_agent",
        "reject": "requirements_agent"
    }
)



builder.add_edge(
    "architecture_agent",
    END
)



#Checkpoint us the Sqlite for ram store

checkpointer = SqliteSaver(
    sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
)

graph = builder.compile(
    checkpointer=checkpointer
)