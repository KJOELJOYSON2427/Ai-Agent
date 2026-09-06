from app.graph.workflow import graph


initial_state = {
    "messages": [],
    "requirement": "Build a courier management system",
    "requirements": "",
    "next_step": "",
    "architecture": "",
}


result = graph.invoke(initial_state)


print("\n========== ARCHITECTURE ==========\n")
print(result["architecture"])


print("\n========== MESSAGES ==========\n")

for message in result["messages"]:
    print("Type:", type(message).__name__)
    print("Content:", message.content)
    print()