import json
import os
import faiss
import sqlite3
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
metadata = []

# TXT files
for file in os.listdir("docs"):
    if file.endswith(".txt"):
        path = f"docs/{file}"
        with open(path, "r", encoding="utf-8") as f:
            for line in f.read().split("\n"):
                if line.strip():
                    documents.append(line)
                    metadata.append({
                        "source": file,
                        "type": "txt"
                    })

# PDF files
for file in os.listdir("docs"):
    if file.endswith(".pdf"):
        reader = PdfReader(f"docs/{file}")
        for page_no, page in enumerate(reader.pages):
            for line in page.extract_text().split("\n"):
                if line.strip():
                    documents.append(line)
                    metadata.append({
                        "source": file,
                        "type": "pdf",
                        "page": page_no + 1
                    })

# SQLite KB
conn = sqlite3.connect("knowledge.db")
cursor = conn.cursor()
cursor.execute("SELECT id, content FROM knowledge")
rows = cursor.fetchall()
conn.close()

for row_id, text in rows:
    documents.append(text)
    metadata.append({
        "source": "knowledge.db",
        "type": "sqlite",
        "row_id": row_id
    })

# Embeddings
embeddings = model.encode(documents)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "vector.index")

# Save metadata
with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("✅ Ingested with metadata tracking")
