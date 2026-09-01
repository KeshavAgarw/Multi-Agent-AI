# 🤖 Multi-Agent Customer Support Automation System

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.28-orange?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Gemini-AI-0088CC?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)

> An intelligent, autonomous customer support system powered by **LangGraph** and **Google Gemini**, designed to handle complex customer queries through multi-agent orchestration, intent classification, and Retrieval-Augmented Generation (RAG).

<div align="center">
  <img src="./Screenhots%20and%20workflow%20diagram/Workflowdiagram.png" alt="Workflow Diagram" width="800"/>
</div>

## 🌟 Project Highlights

- **Multi-Agent Orchestration**: Built a multi-agent customer support automation system using LangGraph, routing customer queries across 4 specialized agents through intent classification and RAG-based retrieval.
- **Robust Quality Assurance**: Implemented human-in-the-loop approval for high-risk actions and a Supervisor agent to validate agent responses before delivery.

## ✨ Features

- 🧠 **Intent Classification**: Automatically routes incoming queries to the right specialized support "department" (Sales, Tech, Billing, Account).
- 📚 **RAG (Retrieval-Augmented Generation)**: Equips agents with relevant context pulled directly from company documents using FAISS vector search.
- 💾 **Stateful Conversations (SQLite)**: Maintains long-term memory per `customer_id`, allowing the system to recall prior interactions seamlessly.
- ⏸️ **Human-in-the-Loop (HITL)**: Pauses execution for sensitive requests (e.g., refunds, cancellations, escalations) to require manual terminal approval (`approve` / `reject` / `modify`).
- 👔 **Supervisor Agent**: A final QA step that validates the agent's response for quality and accuracy before presenting it to the user.

---

## 🛠️ Project Structure

```text
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
├── memory.db                # Auto-created at runtime
└── ...
```

## 🚀 Setup & Installation

### 1. Prerequisites
- **Python 3.12+**
- A Google Gemini API key

### 2. Environment Setup

It is highly recommended to use a virtual environment:

```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configuration

Copy the example environment file and add your API key:

```powershell
Copy-Item .env.example .env
```

Edit `.env` to include your credentials:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_CHAT_MODEL=models/gemini-2.0-flash
GEMINI_EMBEDDING_MODEL=models/gemini-embedding-001
RAG_K=2
```

> **Note**: Model names are read from `.env` via `config.py`. Adjust them if your API key requires different model IDs.

## 🎯 Running the Demo

Execute the main script to see the agents in action:

```powershell
python main.py
```

### 🔍 What to Expect:
1. **Intelligent Routing**: Query 1 routes to Sales and includes RAG context from the knowledge base docs.
2. **Human Approval**: Query 4 (“refund…”) triggers **HUMAN APPROVAL REQUIRED** and pauses execution. You can choose to `approve`, `reject`, or `modify`.
3. **Memory Retrieval**: Query 5 (“previous issue?”) accesses the **SQLite memory** to provide contextual follow-up.
4. **Audit Trail**: After each query, only the user's prompt and the Supervisor's final response are saved to the SQLite database.

## 💾 SQLite Memory Inspection

The database file `memory.db` is generated at runtime in the project root. To inspect the conversation memory, run:

```powershell
python -c "import sqlite3; c=sqlite3.connect('memory.db'); print(c.execute('select id, customer_id, role, message, timestamp from conversations order by id asc').fetchall())"
```

## ⚠️ Troubleshooting

- **“Missing GOOGLE_API_KEY”**: Ensure the `.env` file is in the project root and properly populated.
- **“models/... not found” (404)**: The selected Gemini model isn't available for your API key. Update `GEMINI_CHAT_MODEL` or `GEMINI_EMBEDDING_MODEL` in `.env` to supported models.

---
*Built with ❤️ using LangGraph and Gemini.*
