import os
import re
import time
from typing import Iterable

from google.api_core.exceptions import ResourceExhausted
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from config import get_chat_model, get_google_api_key

_MAX_RETRIES = 3


def _retry_delay_seconds(error: ResourceExhausted) -> float:
    match = re.search(r"retry in ([0-9.]+)s", str(error), re.IGNORECASE)
    if match:
        return float(match.group(1)) + 1.0
    return 5.0


def invoke_chat(messages: Iterable[BaseMessage], *, temperature: float) -> str:
    llm = ChatGoogleGenerativeAI(
        model=get_chat_model(),
        temperature=temperature,
        google_api_key=get_google_api_key(),
    )
    msg_list = list(messages)

    for attempt in range(_MAX_RETRIES):
        try:
            resp = llm.invoke(msg_list)
            return (resp.content or "").strip()
        except ResourceExhausted as e:
            if attempt == _MAX_RETRIES - 1:
                raise RuntimeError(
                    f"Gemini quota exceeded for {get_chat_model()}. "
                    "If the error shows 'limit: 0', this model has no free-tier quota — "
                    "switch GEMINI_CHAT_MODEL to models/gemini-2.0-flash in .env. "
                    f"Original error: {e}"
                ) from e
            delay = _retry_delay_seconds(e)
            print(f"[LLM] Rate limited. Retrying in {delay:.0f}s ({attempt + 1}/{_MAX_RETRIES})...")
            time.sleep(delay)
