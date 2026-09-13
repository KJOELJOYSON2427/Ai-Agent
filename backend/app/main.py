from fastapi import FastAPI
from pydantic import BaseModel

from app.orchestrator.orchestrator import run_orchestrator


class AgentRequest(BaseModel):
    requirement: str


app = FastAPI(title="Software Engineering Agent")



@app.get("/")
def root():
    return {
        "message": "Software Engineering Agent is running"
    }



@app.post("/agent")
def run_agent(request: AgentRequest):

    result = run_orchestrator(request.requirement)

    return {
        "requirement": request.requirement,
        "response": result
    }


