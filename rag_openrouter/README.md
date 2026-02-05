# 📘 RAG System + Prompt Engineering using OpenRouter (Free Models)

## 🔥 Overview

This repository contains an **end-to-end Retrieval Augmented Generation (RAG) system** built using **only free and open-source tools**.

It demonstrates:
- Core **Prompt Engineering techniques**
- Calling LLMs using **OpenRouter.ai (free models)**
- Document ingestion (TXT + PDF)
- Chunking & embeddings
- SQLite-based knowledge base
- Source attribution (answer traceability)
- **FastAPI backend**
- **Streamlit UI**

❌ No paid APIs  
❌ No vendor lock-in  
✅ Interview & production ready  

---

## 🧠 Prompt Engineering Techniques Covered

### 1️⃣ Zero-Shot Prompting
No examples, only instruction.

```text
Explain chunking in RAG systems.
OpenRouter LLM Integration
Why OpenRouter?

Free access to models

OpenAI-compatible API

Easy model switching

Model Used
openai/gpt-3.5-turbo

LLM Call Flow
User Question
   ↓
Prompt Builder
   ↓
OpenRouter API
   ↓
LLM Response

🔐 Environment Setup
.env
OPENROUTER_API_KEY=sk-xxxx
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions

.gitignore
.env
__pycache__/
*.db

📄 Document Ingestion

Supported formats:

.txt

.pdf

Dummy knowledge files:

docs/
 ├── ai_basics.txt
 ├── rag_intro.txt
 ├── embeddings.txt
 ├── llm_working.txt
 └── fastapi_notes.txt


PDF parsing is done using PyPDF2.

✂️ Chunking (WHY & HOW)
Why Chunking?

LLM context window limits

Better semantic matching

Improved retrieval accuracy

How?
chunk_size = 500
overlap = 50


Each chunk stores:

text

source file

chunk index

🧮 Embeddings (WHY & HOW)
Why Embeddings?

LLMs cannot directly search text.

Embeddings convert text into vectors so we can:

Perform similarity search

Retrieve relevant context

Flow
Text Chunk
   ↓
Embedding
   ↓
Vector
   ↓
SQLite DB

🗃 SQLite Knowledge Base
Tables
documents(id, content, source)
embeddings(id, vector, document_id)

Why SQLite?

Lightweight

No server needed

Ideal for local & demo RAG systems

🔍 Retrieval Process (RAG Core)
User Question
   ↓
Question Embedding
   ↓
Similarity Search (Top-K)
   ↓
Relevant Chunks
   ↓
Prompt Injection
   ↓
LLM Answer

🧾 Source Attribution

Each chunk includes metadata:

filename

page number (PDF)

chunk index

Final response contains:

Answer + Source file name


Benefits:

Explainability

Debugging

Trustworthy AI

⚙️ FastAPI Backend
Endpoints
/ingest

Reads documents

Chunks text

Stores embeddings

/ask

Accepts user question

Performs RAG

Returns answer + source

FastAPI provides scalability and production readiness.

🖥 Streamlit UI

Features:

Upload documents

Ask questions

View answers

See source attribution

Why Streamlit?

Fast prototyping

ML-friendly

Perfect for demos

