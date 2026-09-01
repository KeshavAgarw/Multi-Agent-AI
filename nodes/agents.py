from langchain_core.messages import HumanMessage, SystemMessage

from llm import invoke_chat
from memory.sqlite_memory import format_history_for_prompt, get_history

HIGH_RISK_KEYWORDS = [
    "refund",
    "cancel",
    "cancellation",
    "close account",
    "account closure",
    "compensation",
    "escalate",
    "escalation",
]


def _check_requires_approval(query: str) -> bool:
    q = query.lower()
    return any(k in q for k in HIGH_RISK_KEYWORDS)


def _run_agent(state: dict, department: str, system_prompt: str) -> dict:
    query = state["customer_query"]
    context = state.get("retrieved_context") or "No context available."
    history_text = format_history_for_prompt(state.get("conversation_history", []))
    requires_approval = _check_requires_approval(query)

    full_prompt = f"""{system_prompt}

Relevant knowledge base information:
{context}

Previous conversation history:
{history_text}"""

    messages = [
        SystemMessage(content=full_prompt),
        HumanMessage(content=query),
    ]

    agent_response = invoke_chat(messages, temperature=0.3)

    print(f"[{department} Agent] Response generated. Requires approval: {requires_approval}")

    return {
        **state,
        "department": department,
        "agent_response": agent_response,
        "requires_approval": requires_approval,
        "approval_status": "pending" if requires_approval else "not_required",
    }


def sales_agent(state: dict) -> dict:
    return _run_agent(
        state,
        "Sales",
        """You are a Sales Support specialist at ABC Technologies.
Help customers with pricing plans, subscription options, and product information.
Be enthusiastic but accurate. Always mention the free trial if relevant.""",
    )


def technical_agent(state: dict) -> dict:
    return _run_agent(
        state,
        "Technical Support",
        """You are a Technical Support specialist at ABC Technologies.
Help customers troubleshoot application errors, crashes, installation issues, and configuration problems.
Provide step-by-step solutions. Be clear and patient.""",
    )


def billing_agent(state: dict) -> dict:
    return _run_agent(
        state,
        "Billing",
        """You are a Billing Support specialist at ABC Technologies.
Help customers with invoices, payments, and billing queries.
For refund requests, inform the customer that their request will be reviewed by a supervisor.""",
    )


def account_agent(state: dict) -> dict:
    return _run_agent(
        state,
        "Account",
        """You are an Account Support specialist at ABC Technologies.
Help customers with password resets, profile updates, and account management.
Provide clear step-by-step instructions.""",
    )


def memory_agent(state: dict) -> dict:
    customer_id = state["customer_id"]
    history = get_history(customer_id)
    history_text = format_history_for_prompt(history)

    if not history:
        response = (
            "I don't have any previous conversations on record for you. "
            "This might be our first interaction, or your history may have been cleared."
        )
    else:
        messages = [
            SystemMessage(
                content=f"""You are a customer support assistant.
The customer is asking about their previous support interactions.
Here is their full conversation history:

{history_text}

Answer their question based on this history."""
            ),
            HumanMessage(content=state["customer_query"]),
        ]
        response = invoke_chat(messages, temperature=0.3)

    print(f"[Memory Agent] Recalled history for customer: {customer_id}")

    return {
        **state,
        "conversation_history": history,
        "department": "Memory Recall",
        "agent_response": response,
        "requires_approval": False,
        "approval_status": "not_required",
    }
