# AI-Powered Customer Support System (LangGraph)

This project is a multi-agent customer support chatbot built with **LangGraph** (Python).

It demonstrates:
- **Intent classification** → routes queries to the right support “department”
- **RAG (Retrieval Augmented Generation)** → pulls relevant context from company docs
- **SQLite conversation memory** → remembers prior messages per `customer_id`
- **Human-in-the-loop approval** → pauses for sensitive requests (refund/cancel/close/compensation/escalation)

## Requirements
- **Python 3.12**
- A Gemini API key in `.env` as `GOOGLE_API_KEY=...`

Pinned dependencies are in `requirements.txt`:
- `langgraph==0.2.28`
- `langchain==0.3.7`
- `langchain-google-genai==2.0.4`
- `langchain-community==0.3.7`
- `faiss-cpu==1.8.0`
- `python-dotenv==1.0.1`

## Project structure

```
customer_support/
├── main.py                  # CLI entry point (runs 5 demo queries)
├── graph.py                 # LangGraph workflow definition
├── state.py                 # Shared graph state + initial_state()
├── llm.py                   # Gemini chat wrapper w/ model fallback
├── nodes/
│   ├── classifier.py        # Intent classifier (LLM with heuristic fallback)
│   ├── router.py            # Intent → agent routing
│   ├── agents.py            # Sales/Tech/Billing/Account/Memory agents
│   ├── supervisor.py        # Supervisor QA (LLM with fallback)
│   └── human_approval.py    # Human approval pause (input(); EOF-safe)
├── rag/
│   ├── documents.py         # Fake company documents (knowledge base)
│   └── retriever.py         # FAISS retriever w/ keyword fallback
├── memory/
│   └── sqlite_memory.py     # SQLite memory store (customer-scoped)
├── scripts/
│   ├── memory_smoke_test.py
│   ├── rag_smoke_test.py
│   └── classifier_smoke_test.py
├── memory.db                # Auto-created at runtime
├── requirements.txt
├── .env                     # Your key (NOT committed)
├── .env.example
└── .gitignore
```

## Setup

### 1) Create a virtual environment (recommended)

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies (pinned)

```powershell
pip install -r requirements.txt
```

### 3) Create `.env`

Copy the example:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set:

```text
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_CHAT_MODEL=models/gemini-2.0-flash
GEMINI_EMBEDDING_MODEL=models/gemini-embedding-001
RAG_K=2
```

Model names are read from `.env` via `config.py` — change them there if your API key uses different model IDs.

## Run the demo

```powershell
python main.py
```

### What you should see
- Query 1 routes to Sales and includes RAG context from docs
- Query 4 (“refund…”) triggers **HUMAN APPROVAL REQUIRED** and pauses for:
  - `approve` / `reject` / `modify`
- Query 5 (“previous issue?”) answers using **SQLite memory**
- After each query, the project saves **only**:
  - the user query (`role="user"`)
  - the supervisor final response (`role="assistant"`)

## SQLite memory output (for submission screenshots)

The DB file is created at:
- `memory.db` in the project root

You can inspect it with Python quickly:

```powershell
python -c "import sqlite3; c=sqlite3.connect('memory.db'); print(c.execute('select id, customer_id, role, message, timestamp from conversations order by id asc').fetchall())"
```

## Human approval behavior

Sensitive requests are detected by **keywords only** (tight scope):

- refund
- cancel / cancellation
- close account / account closure
- compensation
- escalate / escalation

When detected, the graph routes to `nodes/human_approval.py` and pauses for terminal input (`approve` / `reject` / `modify`).

## Configuration

All runtime settings are loaded from `.env` through `config.py`:

| Variable | Default | Purpose |
|---|---|---|
| `GOOGLE_API_KEY` | *(required)* | Gemini API key |
| `GEMINI_CHAT_MODEL` | `models/gemini-2.0-flash` | Chat model for classifier, agents, supervisor |
| `GEMINI_EMBEDDING_MODEL` | `models/gemini-embedding-001` | Embedding model for FAISS RAG |
| `RAG_K` | `2` | Number of document chunks retrieved per query |

## Troubleshooting

### “Missing GOOGLE_API_KEY”
- Ensure `.env` exists in the project root and contains `GOOGLE_API_KEY=...`
- Re-run:

```powershell
python main.py
```

### “models/... not found” (NotFound / 404)
The model ID in your `.env` is not available for your API key. Update `GEMINI_CHAT_MODEL` or `GEMINI_EMBEDDING_MODEL` to a model your key supports.

