import sqlite3

conn = sqlite3.connect("knowledge.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT
)
""")

data = [
    ("FAISS is a library for efficient similarity search.",),
    ("SQLite is a lightweight relational database.",),
    ("RAG improves accuracy by grounding LLM responses.",),
    ("FastAPI is used to build high-performance APIs.",)
]

cursor.executemany("INSERT INTO knowledge (content) VALUES (?)", data)

conn.commit()
conn.close()

print("✅ Knowledge base created & populated")
