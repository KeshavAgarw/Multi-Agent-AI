def human_approval_node(state: dict) -> dict:
    print("\n" + "=" * 60)
    print("HUMAN APPROVAL REQUIRED")
    print("=" * 60)
    print(f"Customer ID: {state['customer_id']}")
    print(f"Customer Query: {state['customer_query']}")
    print(f"Department: {state.get('department')}")
    print(f"\nDraft Response from Agent:\n{state.get('agent_response')}")
    print("=" * 60)

    while True:
        decision = (
            input("\nSupervisor Action — Enter 'approve', 'reject', or 'modify': ")
            .strip()
            .lower()
        )

        if decision == "approve":
            print("[Human Approval] Request APPROVED")
            return {
                **state,
                "approval_status": "approved",
                "human_feedback": "Approved by supervisor.",
            }

        if decision == "reject":
            reason = input("Enter rejection reason: ").strip()
            print("[Human Approval] Request REJECTED")
            return {
                **state,
                "approval_status": "rejected",
                "human_feedback": reason,
                "agent_response": (
                    "We're sorry, but your request could not be approved at this time. "
                    f"Reason: {reason}"
                ),
            }

        if decision == "modify":
            new_response = input("Enter modified response to send to customer:\n> ").strip()
            print("[Human Approval] Response MODIFIED")
            return {
                **state,
                "approval_status": "approved",
                "agent_response": new_response,
                "human_feedback": "Response modified by supervisor.",
            }

        print("Invalid input. Please enter 'approve', 'reject', or 'modify'.")


def needs_approval(state: dict) -> str:
    if state.get("requires_approval") and state.get("approval_status") == "pending":
        return "human_approval"
    return "supervisor"
