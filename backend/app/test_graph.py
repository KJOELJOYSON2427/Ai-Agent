import time
from app.graph.workflow import graph
from langgraph.types import Command
from google.genai import errors  # Make sure to import this to catch the API error

config = {
    "configurable": {
        "thread_id": "project-001"
    }
}

# -----------------------------
# 0. Safe Invoke Helper Function
# -----------------------------
def invoke_graph_with_retry(input_data, graph_config):
    """
    Wraps graph.invoke to catch 429 Resource Exhausted errors
    and wait out the rate-limit penalty automatically.
    """
    while True:
        try:
            return graph.invoke(input_data, config=graph_config)
        except errors.ClientError as e:
            # Check if it's a 429 Quota Exceeded error
            if e.code == 429:
                print("\n⚠️ [Rate Limit Hit] Daily/Minute quota exhausted.")
                print("⏳ Waiting 40 seconds before retrying the step...")
                time.sleep(40)
                print("🔄 Retrying workflow step now...")
            else:
                # Raise any other ClientError (like 400 Bad Request, 403 Forbidden)
                raise e
        except Exception as e:
            # Catch other unexpected errors
            raise e

# -----------------------------
# 1. Start the project (Uses the timer helper)
# -----------------------------
result = invoke_graph_with_retry(
    {
        "messages": [],
        "requirement": "Build a courier management system",
        "requirements": "",
        "architecture": "",
        "next_step": "",
        "review_feedback": ""
    },
    graph_config=config
)


# -----------------------------
# 2. Human review loop
# -----------------------------
while True:

    state = graph.get_state(config)

    print("\nNEXT:", state.next)

    if "human_review" not in state.next:
        break

    print("\n===== REQUIREMENTS =====")
    print(state.values["requirements"])

    print("\n===== HUMAN REVIEW =====")
    decision = input("Approve or reject? ").strip().lower()

    while decision not in ["approve", "reject"]:
        decision = input("Please enter 'approve' or 'reject': ").strip().lower()

    # Uses the timer helper to resume the graph safely
    result = invoke_graph_with_retry(
        Command(resume=decision),
        graph_config=config
    )


# -----------------------------
# 3. Final state
# -----------------------------
state = graph.get_state(config)

print("\n===== GRAPH FINISHED =====")
print("NEXT:", state.next)

print("\n===== ARCHITECTURE =====")
print(state.values.get("architecture"))
