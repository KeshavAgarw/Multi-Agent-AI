from typing import List, Optional, TypedDict


class SupportState(TypedDict):
    # Customer info
    customer_id: str
    customer_query: str

    # Classification result
    intent: Optional[str]  # "Sales", "Technical", "Billing", "Account", "Memory"

    # RAG context
    retrieved_context: Optional[str]

    # Which agent handled it
    department: Optional[str]

    # Agent's draft response
    agent_response: Optional[str]

    # Human approval
    requires_approval: bool
    approval_status: Optional[str]  # "pending", "approved", "rejected", "not_required"
    human_feedback: Optional[str]

    # Final output
    final_response: Optional[str]

    # Conversation history (for memory)
    conversation_history: List[dict]


def initial_state(customer_id: str, query: str) -> SupportState:
    return {
        "customer_id": customer_id,
        "customer_query": query,
        "intent": None,
        "retrieved_context": None,
        "department": None,
        "agent_response": None,
        "requires_approval": False,
        "approval_status": None,
        "human_feedback": None,
        "final_response": None,
        "conversation_history": [],
    }
