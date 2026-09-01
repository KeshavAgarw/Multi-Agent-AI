from langchain_core.messages import HumanMessage, SystemMessage

from llm import invoke_chat


def supervisor_agent(state: dict) -> dict:
    query = state["customer_query"]
    draft = state.get("agent_response") or ""
    approval_status = state.get("approval_status", "not_required")

    if approval_status == "rejected":
        print("[Supervisor] Request was rejected by human. Finalizing rejection response.")
        return {**state, "final_response": draft}

    messages = [
        SystemMessage(
            content="""You are the Quality Assurance Supervisor at ABC Technologies.
Review the draft response from the support agent and improve it if needed.

Your job:
1. Ensure the response is professional and polite
2. Ensure it actually answers the customer's question
3. Add empathy where appropriate (e.g., 'We understand this is frustrating...')
4. Ensure no incorrect promises are made
5. Keep it concise — no more than 200 words

Return ONLY the final improved response. Do not add any commentary or labels."""
        ),
        HumanMessage(
            content=f"""Customer Query: {query}

Agent Draft Response:
{draft}

Please review and return the final improved response."""
        ),
    ]

    final_response = invoke_chat(messages, temperature=0.2)
    print("[Supervisor] Response reviewed and finalized.")

    return {**state, "final_response": final_response}
