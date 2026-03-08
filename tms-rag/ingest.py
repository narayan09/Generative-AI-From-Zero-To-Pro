
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_NAME = os.getenv("DB_NAME")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# 1. Connect to MySQL
connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

#connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
#engine = create_engine(connection_string)

try:
    engine = create_engine(connection_string)

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    print("✅ Database connection successful")

except Exception as e:
    print("❌ Database connection failed")
    print(e)

# 2. Define a function to convert a row to text
def row_to_text(table, row):
    if table == 'shipments':
        return (f"Shipment {row['shipment_id']} for order {row['order_id']} from {row['origin']} to {row['destination']}. "
                f"Shipped on {row['shipment_date']}, delivered on {row['delivery_date'] or 'not yet'}. Status: {row['status']}.")
    elif table == 'parcels':
        return (f"Parcel {row['parcel_id']} in shipment {row['shipment_id']} weighs {row['weight']}kg, dimensions {row['dimensions']}, "
                f"content type: {row['content_type']}.")
    elif table == 'tracking_events':
        return (f"Tracking event for shipment {row['shipment_id']}: at {row['location']} on {row['timestamp']}, status: {row['status']}.")
    elif table == 'delivery_agents':
        return (f"Delivery agent {row['agent_id']}: {row['name']}, phone {row['phone']}, vehicle {row['vehicle_number']}.")
    elif table == 'warehouses':
        return (f"Warehouse {row['warehouse_id']}: {row['name']} in {row['city']}, capacity {row['capacity']}.")
    else:
        return str(row)

# 3. Load all tables and create documents
tables = ['shipments', 'parcels', 'tracking_events', 'delivery_agents', 'warehouses']
documents = []

for table in tables:
    print(f"Loading {table}...")

    with engine.connect() as conn:
        df = pd.read_sql(text(f"SELECT * FROM {table}"), conn)

    for _, row in df.iterrows():
        #text = row_to_text(table, row)
        doc_text = row_to_text(table, row)

        id_col = f"{table[:-1]}_id"
        if table == "tracking_events":
            id_col = "tracking_id"

        metadata = {
            "table": table,
            "id": str(row.get(id_col, ""))
        }

        doc = Document(page_content=doc_text, metadata=metadata)
        documents.append(doc)
print(f"Total documents created: {len(documents)}")

# 4. Create embeddings and store in ChromaDB
embedding_function = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding_function,
    persist_directory=CHROMA_PERSIST_DIR,
    collection_name="tms_docs"
)

vectorstore.persist()
print(f"Vector store saved to {CHROMA_PERSIST_DIR}")