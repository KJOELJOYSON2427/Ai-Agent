from app.state.state import AgentState

def route_after_requirements(state: AgentState):
    return state["next_step"]



def route_from_orchestrator(state: AgentState):

    return state["next_step"]