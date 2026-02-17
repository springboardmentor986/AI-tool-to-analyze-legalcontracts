from langgraph.graph import StateGraph

def classify_contract(state):
    return {"stage": "classified"}

graph = StateGraph(dict)
graph.add_node("classify_contract", classify_contract)
graph.set_entry_point("classify_contract")
graph.set_finish_point("classify_contract")

app = graph.compile()

print(app.invoke({}))
