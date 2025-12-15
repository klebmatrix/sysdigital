from langgraph.graph import StateGraph
from graph.state import ResearchState
from graph.nodes import *

def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("intent", intent_clarification)
    graph.add_node("brief", research_brief)
    graph.add_node("draft", initial_draft)
    graph.add_node("pedagogical_review", pedagogical_denoising)
    graph.add_node("converge", convergence_check)
    graph.add_node("final", finalize)

    graph.set_entry_point("intent")
    graph.add_edge("intent", "brief")
    graph.add_edge("brief", "draft")
    graph.add_edge("draft", "pedagogical_review")
    graph.add_edge("pedagogical_review", "converge")

    graph.add_conditional_edges(
        "converge",
        lambda s: "final" if s["approved"] else "draft"
    )

    graph.set_finish_point("final")
    return graph.compile()
