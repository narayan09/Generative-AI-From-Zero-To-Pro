import faiss
import requests
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import json

load_dotenv()  # load .env file

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL")
MODEL_NAME = os.getenv("MODEL")

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("vector.index")
with open("chunks.txt", "r", encoding="utf-8") as f:
    chunks = f.readlines()

with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)


def retrieve_context_with_sources(query, k=3):
    q_embed = model.encode([query])
    _, indices = index.search(q_embed, k)

    results = []
    for idx in indices[0]:
        results.append({
            "text": chunks[idx].strip(),
            "source": metadata[idx]
        })

    return results

def ask_llm_with_citations(context_chunks, question):
    context_text = ""
    distances = []

    for i, item in enumerate(context_chunks):
        context_text += f"[{i+1}] {item['text']}\n"
        distances.append(item.get("distance", 0.5))

    prompt = f"""
You are a RAG-based assistant.
Answer ONLY using the context.
Add citation numbers like [1], [2].
If not found, say "I don't know".

Context:
{context_text}

Question:
{question}
"""

    answer = call_openrouter(prompt)

    avg_distance = sum(distances) / len(distances) if distances else 1
    confidence = round(min(1.0, 1 / (1 + avg_distance)), 2)

    sources = [item["source"] for item in context_chunks]

    return answer, confidence, sources

def call_openrouter(prompt: str) -> str:
    
    """
    Sends prompt to OpenRouter and returns model response
    """

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",   # required by OpenRouter
        "X-Title": "RAG Demo App"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"OpenRouter Error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]


def ask_llm(context, question):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    context_text = ""
    citations = []

    for i, item in enumerate(context):
        context_text += f"[{i+1}] {item['text']}\n"
        citations.append(item["source"])

    prompt = f"""
Answer the question using ONLY the context below.
Mention reference numbers like [1], [2].

Context:
{context_text}

Question:
{question}
"""

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }

    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]
