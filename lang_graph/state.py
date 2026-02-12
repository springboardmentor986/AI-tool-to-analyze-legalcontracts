from typing import TypedDict, List

class GraphState(TypedDict):
    text: str
    agents: List[str]
    results: dict