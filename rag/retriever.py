from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import get_embedding_model, get_google_api_key, get_rag_k
from rag.documents import DOCUMENTS


def build_vectorstore() -> FAISS:
    model = get_embedding_model()
    docs = [
        Document(page_content=d["content"], metadata={"source": d["source"]})
        for d in DOCUMENTS
    ]
    embeddings = GoogleGenerativeAIEmbeddings(
        model=model,
        google_api_key=get_google_api_key(),
    )
    print(f"[RAG] Using embedding model: {model}")
    return FAISS.from_documents(docs, embeddings)


def retrieve_context(query: str, vectorstore: FAISS, k: int | None = None) -> str:
    k = k if k is not None else get_rag_k()
    results = vectorstore.similarity_search(query, k=k)
    if not results:
        return "No relevant information found in knowledge base."

    context_parts: list[str] = []
    for doc in results:
        context_parts.append(
            f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content.strip()}"
        )
    return "\n\n".join(context_parts)
