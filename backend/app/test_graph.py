# from app.graph.workflow import graph


# initial_state = {
#     "messages": [],
#     "requirement": "Build a courier management system",
#     "requirements": "",
#     "next_step": "",
#     "architecture": "",
# }


# result = graph.invoke(initial_state)


# print("\n========== ARCHITECTURE ==========\n")
# print(result["architecture"])


# print("\n========== MESSAGES ==========\n")

# for message in result["messages"]:
#     print("Type:", type(message).__name__)
#     print("Content:", message.content)
#     print()


from app.graph.workflow import graph

config = {
    "configurable": {
        "thread_id": "project-001"
    }
}

result = graph.invoke(
    {
        "messages": [],
        "requirement": "Build a courier management system",
        "requirements": "",
        "architecture": "",
        "next_step": "",
        "review_feedback": ""
    },
    config=config
)


state = graph.get_state({
    "configurable": {
        "thread_id": "project-001"
    }
})

print("STATE:")
print(state.values)

print("NEXT:")
print(state.next)