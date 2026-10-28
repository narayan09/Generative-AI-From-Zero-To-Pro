# ingest_documents.py
import os
import glob
import ollama
import chromadb
from dotenv import load_dotenv

load_dotenv()

DOCUMENTS_FOLDER = "documents"
CHROMA_DB_PATH = "chroma_db"
COLLECTION_NAME = "jira_docs"
EMBEDDING_MODEL = "nomic-embed-text"   # Ollama model

def load_documents(folder):
    docs = []
    for filepath in glob.glob(os.path.join(folder, "**/*.*"), recursive=True):
        if filepath.endswith(('.txt', '.md', '.rst')):
            with open(filepath, 'r', encoding='utf-8') as f:
                docs.append((filepath, f.read()))
        elif filepath.endswith('.pdf'):
            from pypdf import PdfReader
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            docs.append((filepath, text))
    return docs

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def get_embedding(text: str) -> list[float]:
    """Get embedding from Ollama."""
    response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
    return response['embedding']

def ingest():
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    docs = load_documents(DOCUMENTS_FOLDER)
    print(f"Found {len(docs)} documents.")

    for filepath, content in docs:
        chunks = chunk_text(content)
        print(f"Processing {filepath}: {len(chunks)} chunks")
        ids = [f"{os.path.basename(filepath)}_{i}" for i in range(len(chunks))]
        # Generate embeddings for each chunk
        embeddings = [get_embedding(chunk) for chunk in chunks]
        # Upsert into collection
        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=[{"source": filepath, "chunk": i} for i in range(len(chunks))],
            documents=chunks
        )

    print(f"Ingestion complete. Collection size: {collection.count()}")

if __name__ == "__main__":
    ingest()