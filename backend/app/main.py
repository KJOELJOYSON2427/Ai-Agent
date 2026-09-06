# from fastapi import FastAPI
# from pydantic import BaseModel

# from app.agents.orchestrator import run_orchestrator


# class AgentRequest(BaseModel):
#     requirement: str


# app = FastAPI(title="Software Engineering Agent")



# @app.get("/")
# def root():
#     return {
#         "message": "Software Engineering Agent is running"
#     }



# @app.post("/agent")
# def run_agent(request: AgentRequest):
#     result = run_orchestrator(request.requirement)

#     return {
#         "requirement": request.requirement,
#         "response": result
#     }


from app.graph.workflow import graph   

result = graph.invoke({                
    "messages": [],
    "requirement": "Build a courier management system",
    "requirements": ""
})
text = result["messages"][-1].content[0]["text"]

print(text)