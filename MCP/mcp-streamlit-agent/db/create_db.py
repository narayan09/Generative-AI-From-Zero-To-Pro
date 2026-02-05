import sqlite3

conn = sqlite3.connect("db/data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT,
    location TEXT
)
""")

data = [
    ("Amit Sharma", "Data Engineer", "Delhi"),
    ("Neha Verma", "ML Engineer", "Bangalore"),
    ("Rahul Singh", "Backend Developer", "Mumbai"),
    ("Priya Patel", "AI Researcher", "Pune")
]

cursor.executemany(
    "INSERT INTO employees (name, role, location) VALUES (?, ?, ?)",
    data
)

conn.commit()
conn.close()

print("✅ Database created and data inserted")
