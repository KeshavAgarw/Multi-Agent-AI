import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root before anything else
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# Add project root to path so imports work
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag.retriever import build_vectorstore, retrieve_context


def main() -> None:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing GOOGLE_API_KEY. Check that .env exists in the project root "
            "and contains: GOOGLE_API_KEY=your_actual_key_here"
        )

    print(f"[OK] API key loaded: {api_key[:8]}...")

    vs = build_vectorstore()
    print("[OK] Vectorstore built successfully")

    queries = [
        "What are your pricing plans?",
        "I need a refund for my annual subscription.",
        "My application crashes when I upload a file.",
    ]
    for q in queries:
        print("\n" + "=" * 60)
        print(q)
        print("-" * 60)
        print(retrieve_context(q, vs, k=2)[:800])


if __name__ == "__main__":
    main()