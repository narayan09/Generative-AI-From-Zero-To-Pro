# rag_retriever.py
import os
import ollama
import chromadb
from dotenv import load_dotenv
from llm_interface import LLMInterface

load_dotenv()

CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "jira_docs"
EMBEDDING_MODEL = "nomic-embed-text"
TOP_K = 3

class RAGRetriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection = self.client.get_collection(COLLECTION_NAME)
        self.llm = LLMInterface()

    def _get_embedding(self, text: str):
        response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
        return response['embedding']

    def retrieve(self, question: str, k=TOP_K):
        query_embedding = self._get_embedding(question)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        if results['documents'] and results['documents'][0]:
            return results['documents'][0]
        return []

    def generate_answer(self, question: str):
        context_chunks = self.retrieve(question)
        if not context_chunks:
            return "I couldn't find any relevant documents.", []

        context = "\n\n".join(context_chunks)
        system_prompt = (
            "You are a helpful Jira expert assistant. Answer the user's question using ONLY the context below. "
            "If the answer is not in the context, say you don't know. Do not use any outside knowledge.\n\n"
            f"Context:\n{context}"
        )
        try:
            answer = self.llm.chat(system_prompt, question)
            return answer, context_chunks
        except Exception as e:
            return f"Sorry, I encountered an error: {e}", context_chunks