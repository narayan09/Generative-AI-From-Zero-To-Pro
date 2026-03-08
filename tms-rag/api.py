from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import RAGPipeline


app = FastAPI(title="TMS RAG API")

# Initialize the RAG pipeline once (it loads the vector store)
rag = RAGPipeline()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]  # list of first 100 chars of source docs

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        result = rag.query(request.question)
        sources = [doc.page_content[:100] + "..." for doc in result["source_documents"]]
        return QueryResponse(answer=result["answer"], sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)