from langgraph.types import interrupt

from app.state.state import AgentState


def human_review(state: AgentState):

    decision = interrupt({
        "message": "Please review the requirements.",
        "requirements": state["requirements"],
        "options": ["approve", "reject"]
    })

    if decision not in ["approve", "reject"]:
            raise ValueError("Decision must be 'approve' or 'reject'")

    return {
        "next_step": decision
    }