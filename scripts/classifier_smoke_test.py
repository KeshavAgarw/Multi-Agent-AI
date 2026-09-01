import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv

from memory.sqlite_memory import init_db, save_message
from nodes.classifier import classify_intent
from state import initial_state


def main() -> None:
    load_dotenv()

    init_db()

    customer_id = "CUST_CLASSIFY"
    save_message(customer_id, "user", "Yesterday I had login issues.")
    save_message(customer_id, "assistant", "Try clearing cache and using incognito.")

    tests = [
        "What are the pricing plans?",
        "I forgot my account password.",
        "My application crashes whenever I upload a file.",
        "I need a refund for my annual subscription.",
        "What was my previous support issue?",
    ]

    for q in tests:
        s = initial_state(customer_id, q)
        out = classify_intent(s)
        print(f"Query: {q}")
        print(f"Intent: {out.get('intent')}")
        print("-" * 40)


if __name__ == "__main__":
    main()

