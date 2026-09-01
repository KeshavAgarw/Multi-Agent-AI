from langchain_core.messages import HumanMessage, SystemMessage

from llm import invoke_chat
from memory.sqlite_memory import format_history_for_prompt, get_history


def classify_intent(state: dict) -> dict:
    query = state["customer_query"]
    customer_id = state["customer_id"]

    history = get_history(customer_id)
    history_text = format_history_for_prompt(history)

    system_prompt = """You are a customer support classifier for ABC Technologies.

Classify the customer query into EXACTLY ONE of these categories:
- Sales: pricing, plans, subscriptions, product info
- Technical: app errors, crashes, installation, login, configuration
- Billing: invoices, payments, refunds, billing issues
- Account: password reset, profile, account activation/deactivation
- Memory: customer is asking about their previous conversation or past issues

Previous conversation history:
{history}

Respond with ONLY the category name. Nothing else. No explanation."""

    messages = [
        SystemMessage(content=system_prompt.format(history=history_text)),
        HumanMessage(content=f"Customer query: {query}"),
    ]

    intent = invoke_chat(messages, temperature=0)

    valid_intents = ["Sales", "Technical", "Billing", "Account", "Memory"]
    if intent not in valid_intents:
        intent = "Technical"

    print(f"[Classifier] Intent detected: {intent}")

    return {
        **state,
        "intent": intent,
        "conversation_history": history,
    }
