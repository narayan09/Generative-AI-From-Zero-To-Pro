from fastapi import FastAPI
from rag_utils import retrieve_context_with_sources, ask_llm_with_citations

app = FastAPI(title="RAG Backend API")

@app.get("/ask")
def ask(question: str, source_type: str | None = None):
    results = retrieve_context_with_sources(question)

    if source_type:
        results = [r for r in results if r["source"]["type"] == source_type]

    answer, confidence, sources = ask_llm_with_citations(results, question)

    return {
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "sources": sources
    }
