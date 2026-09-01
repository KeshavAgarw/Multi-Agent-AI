from dotenv import load_dotenv

load_dotenv()

from graph import build_graph
from memory.sqlite_memory import init_db, save_message
from state import initial_state


def run_query(app, customer_id: str, query: str) -> dict:
    print("\n" + "=" * 60)
    print(f"Customer ID: {customer_id}")
    print(f"Query: {query}")
    print("=" * 60)

    result = app.invoke(initial_state(customer_id, query))

    final = result.get("final_response") or "No response generated."
    print(f"\nFINAL RESPONSE TO CUSTOMER:\n{final}")

    save_message(customer_id, "user", query)
    save_message(customer_id, "assistant", final)

    return result


if __name__ == "__main__":
    init_db()
    app = build_graph()

    run_query(app, "CUST001", "What are the pricing plans available for your software?")
    run_query(app, "CUST001", "I forgot my account password.")
    run_query(app, "CUST001", "My application crashes whenever I upload a file.")
    run_query(app, "CUST001", "I need a refund for my annual subscription.")
    run_query(app, "CUST001", "What was my previous support issue?")

