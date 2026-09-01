def route_query(state: dict) -> str:
    intent = state.get("intent", "Technical")

    routing_map = {
        "Sales": "sales_agent",
        "Technical": "technical_agent",
        "Billing": "billing_agent",
        "Account": "account_agent",
        "Memory": "memory_agent",
    }

    next_node = routing_map.get(intent, "technical_agent")
    print(f"[Router] Routing to: {next_node}")
    return next_node

