import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from memory.sqlite_memory import DB_PATH, format_history_for_prompt, get_history, init_db, save_message


def main() -> None:
    init_db()
    save_message("CUST_TEST", "user", "Hello")
    save_message("CUST_TEST", "assistant", "Hi there!")
    history = get_history("CUST_TEST")
    print(f"DB: {DB_PATH}")
    print(f"Rows: {len(history)}")
    print(format_history_for_prompt(history))


if __name__ == "__main__":
    main()

