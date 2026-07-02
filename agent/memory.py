from typing import Any

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph


def create_memory() -> MemorySaver:
    return MemorySaver()


def create_graph_with_memory(state_schema: type) -> tuple[StateGraph, MemorySaver]:
    workflow = StateGraph(state_schema)
    memory = create_memory()
    return workflow, memory
