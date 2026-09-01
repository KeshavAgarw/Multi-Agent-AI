import os


def get_google_api_key() -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing GOOGLE_API_KEY. Add it to .env (see .env.example) before running."
        )
    return api_key


def get_chat_model() -> str:
    return os.getenv("GEMINI_CHAT_MODEL", "models/gemini-2.0-flash")


def get_embedding_model() -> str:
    return os.getenv("GEMINI_EMBEDDING_MODEL", "models/gemini-embedding-001")


def get_rag_k() -> int:
    return int(os.getenv("RAG_K", "2"))
