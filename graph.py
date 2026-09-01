from langgraph.graph import END, StateGraph

from nodes.agents import (
    account_agent,
    billing_agent,
    memory_agent,
    sales_agent,
    technical_agent,
)
from nodes.classifier import classify_intent
from nodes.human_approval import human_approval_node, needs_approval
from nodes.router import route_query
from nodes.supervisor import supervisor_agent
from config import get_rag_k
from rag.retriever import build_vectorstore, retrieve_context
from state import SupportState


def build_graph():
    vectorstore = build_vectorstore()
    rag_k = get_rag_k()

    def rag_then_sales(state: dict) -> dict:
        state["retrieved_context"] = retrieve_context(state["customer_query"], vectorstore, k=rag_k)
        return sales_agent(state)

    def rag_then_technical(state: dict) -> dict:
        state["retrieved_context"] = retrieve_context(state["customer_query"], vectorstore, k=rag_k)
        return technical_agent(state)

    def rag_then_billing(state: dict) -> dict:
        state["retrieved_context"] = retrieve_context(state["customer_query"], vectorstore, k=rag_k)
        return billing_agent(state)

    def rag_then_account(state: dict) -> dict:
        state["retrieved_context"] = retrieve_context(state["customer_query"], vectorstore, k=rag_k)
        return account_agent(state)

    graph = StateGraph(SupportState)

    graph.add_node("classifier", classify_intent)
    graph.add_node("sales_agent", rag_then_sales)
    graph.add_node("technical_agent", rag_then_technical)
    graph.add_node("billing_agent", rag_then_billing)
    graph.add_node("account_agent", rag_then_account)
    graph.add_node("memory_agent", memory_agent)
    graph.add_node("human_approval", human_approval_node)
    graph.add_node("supervisor", supervisor_agent)

    graph.set_entry_point("classifier")

    graph.add_conditional_edges(
        "classifier",
        route_query,
        {
            "sales_agent": "sales_agent",
            "technical_agent": "technical_agent",
            "billing_agent": "billing_agent",
            "account_agent": "account_agent",
            "memory_agent": "memory_agent",
        },
    )

    for agent_node in [
        "sales_agent",
        "technical_agent",
        "billing_agent",
        "account_agent",
        "memory_agent",
    ]:
        graph.add_conditional_edges(
            agent_node,
            needs_approval,
            {"human_approval": "human_approval", "supervisor": "supervisor"},
        )

    graph.add_edge("human_approval", "supervisor")
    graph.add_edge("supervisor", END)

    return graph.compile()

