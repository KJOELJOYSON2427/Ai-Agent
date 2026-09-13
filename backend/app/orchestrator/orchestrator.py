from app.graph.workflow import graph
from app.graph.config import config


def run_orchestrator(requirement: str):

    initial_state = {
        "messages": [],
        "requirement": requirement,
        "requirements": "",
        "review_feedback": "",
        "architecture": "",
        "next_step": ""
    }

    result = graph.invoke(initial_state,

                          config=config)

    return result