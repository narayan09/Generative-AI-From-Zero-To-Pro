# 🚚 TMS RAG System – Open Source AI Assistant for Shipment Tracking

A complete, end-to-end **Retrieval-Augmented Generation (RAG)** system designed for a Transportation Management System (TMS). It answers natural language questions about shipments, parcels, and tracking events using data stored in a MySQL database. Built entirely with **free and open-source tools** – no paid APIs or services required.

![Streamlit UI](https://img.shields.io/badge/UI-Streamlit-red)
![FastAPI](https://img.shields.io/badge/API-FastAPI-green)
![LangChain](https://img.shields.io/badge/LangChain-🦜🔗-blue)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-yellow)
![Groq](https://img.shields.io/badge/LLM-Groq%20(Llama3)-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 📖 Table of Contents
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up Python Environment](#2-set-up-python-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Configure MySQL Database](#4-configure-mysql-database)
  - [5. Environment Variables](#5-environment-variables)
  - [6. Ingest Data into Vector Database](#6-ingest-data-into-vector-database)
  - [7. Start the FastAPI Backend](#7-start-the-fastapi-backend)
  - [8. Launch the Streamlit Frontend](#8-launch-the-streamlit-frontend)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [How It Works – Detailed Flow](#how-it-works--detailed-flow)
- [Customization & Extensions](#customization--extensions)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## ✨ Features

- Loads data from **MySQL** tables: `shipments`, `parcels`, `tracking_events`, `delivery_agents`, `warehouses`.
- Converts each database row into a **descriptive text document**.
- Generates embeddings using **sentence-transformers/all-MiniLM-L6-v2** (runs locally on CPU).
- Stores embeddings in a persistent **ChromaDB** vector database.
- Performs **semantic search** to retrieve relevant documents for a user query.
- Augments the prompt with retrieved context and sends it to **Groq's free LLM API** (Llama3 8B or Mixtral).
- Returns a **natural language answer**.
- Provides a **FastAPI** backend for programmatic access.
- Offers a **Streamlit** chat interface for easy interaction.

---

## 🏗️ Architecture Overview

The system follows a classic RAG pipeline:

1. **Data Ingestion**  
   - Python scripts connect to MySQL, read all rows, and transform each row into a text document (e.g., *"Shipment SHP1001 for order ORD1001 from Mumbai to Delhi..."*).
   - Documents are embedded using a local Sentence-Transformer model and stored in ChromaDB with metadata (table name, primary key).

2. **User Query**  
   - User types a question in the Streamlit UI (e.g., *"Where is shipment SHP1002?"*).
   - The question is sent to the FastAPI backend.

3. **Retrieval**  
   - The question is embedded using the same model.
   - ChromaDB performs a similarity search and returns the top‑k most relevant documents.

4. **Augmented Generation**  
   - Retrieved documents are inserted into a prompt template.
   - The full prompt is sent to Groq's LLM (Llama3) via API.
   - The LLM generates an answer based on the provided context.

5. **Response**  
   - The answer (and optionally source documents) is sent back to the UI and displayed to the user.

![Architecture Diagram](docs/architecture.png)  
*(If you prefer a text diagram, see [ASCII representation](#ascii-architecture) below.)*

### ASCII Architecture

---

## 🛠️ Tech Stack

| Component          | Tool                                                                 | Why?                                           |
|--------------------|----------------------------------------------------------------------|------------------------------------------------|
| Language           | Python 3.10+                                                         | Rich ecosystem for ML and web.                 |
| LLM Provider       | [Groq](https://console.groq.com)                                     | Fast, free inference API for Llama3/Mixtral.   |
| LLM Model          | `llama3-8b-8192` (default) or `mixtral-8x7b-32768`                   | High-quality open models.                       |
| Framework          | LangChain                                                            | Simplifies RAG pipeline construction.           |
| Embeddings         | `sentence-transformers/all-MiniLM-L6-v2`                             | Lightweight, runs locally on CPU.               |
| Vector Database    | ChromaDB                                                             | Persistent, local, easy to use.                 |
| Relational Database| MySQL (Community Edition)                                            | Stores structured TMS data.                      |
| Backend API        | FastAPI                                                              | High-performance, easy to develop.              |
| Frontend UI        | Streamlit                                                            | Rapidly build interactive data apps.             |

---

## 📋 Prerequisites

- Python 3.10 or higher
- MySQL server installed and running
- A free [Groq API key](https://console.groq.com) (sign up, get key)
- Git (optional)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tms-rag-system.git
cd tms-rag-system

2. Set Up Python Virtual Environment
bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Configure MySQL Database
Create a database (e.g., tms_db).

Run the provided SQL script to create tables and insert 500 realistic sample records:

bash
mysql -u root -p tms_db < data/sample_data.sql
The script includes tables: shipments, parcels, tracking_events, delivery_agents, warehouses with Indian city names, realistic statuses, and timestamps.

5. Environment Variables
Create a .env file in the project root:

env
# MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=tms_db

# Groq
GROQ_API_KEY=gsk_...   # Replace with your actual key

# Vector store persistence
CHROMA_PERSIST_DIR=./chroma_db
EMBEDDING_MODEL=all-MiniLM-L6-v2

6. Ingest Data into Vector Database
Run the ingestion script to load MySQL data, create embeddings, and store them in ChromaDB:

bash
python ingest.py
7. Start the FastAPI Backend
bash
python api.py
# or
uvicorn api:app --reload
The API will be available at http://localhost:8000.
Test it with:

bash
curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"question": "Where is shipment SHP1002?"}'
8. Launch the Streamlit Frontend
In a new terminal (with the virtual environment activated):

bash
streamlit run ui.py
Open your browser at http://localhost:8501 and start asking questions!

💬 Usage Examples
Once the system is running, you can ask questions like:

“Where is shipment SHP1050?”

“Which shipments are delayed today?”

“Show parcels delivered in Mumbai”

“What is the latest tracking status for shipment SHP1003?”

“How many warehouses are in Delhi?”

“List all delivery agents with vehicle numbers”

“Parcels weighing more than 10kg”

“Give me all tracking events for shipment SHP1002”

The system retrieves relevant records and generates a natural language answer.

📁 Project Structure
text
tms-rag-system/
├── .env                      # Environment variables (not committed)
├── .gitignore
├── requirements.txt          # Python dependencies
├── ingest.py                 # Load MySQL data, embed, store in ChromaDB
├── rag.py                    # RAG pipeline (retriever + Groq LLM)
├── api.py                    # FastAPI application
├── ui.py                     # Streamlit frontend
├── data/
│   └── sample_data.sql       # MySQL dump with 500 sample records
└── chroma_db/                # Created automatically – persists vector index
🔍 How It Works – Detailed Flow
Ingestion Phase
Connect to MySQL using SQLAlchemy.

Read each table (shipments, parcels, ...) into a Pandas DataFrame.

For every row, create a human‑readable text document using a mapping function (e.g., row_to_text).

Add metadata (table name, primary key) to each document.

Embed documents using HuggingFaceEmbeddings (Sentence‑Transformers).

Store in ChromaDB with persistence enabled.

Query Phase
User question sent from Streamlit to FastAPI (/query endpoint).

FastAPI calls the RAGPipeline.query() method.

Retriever (ChromaDB) converts the question to an embedding and returns the top‑k similar documents.

Documents are inserted into a prompt template.

Prompt is sent to Groq's LLM (Llama3) via LangChain's Groq wrapper.

LLM generates answer based on the provided context.

Answer and source documents are returned to the frontend.

Streamlit displays the answer, optionally showing sources in an expander.

🧪 Customization & Extensions
Add more tables: Extend row_to_text in ingest.py and update the tables list.

Change LLM model: In rag.py, modify the model parameter (e.g., "mixtral-8x7b-32768").

Adjust number of retrieved documents: Change search_kwargs={"k": 5} in rag.py.

Improve prompt: Edit the prompt_template in rag.py to guide the LLM's behavior.

Metadata filtering: Modify the retriever to filter by table or id for more precise retrieval.

Conversational memory: Integrate LangChain's ConversationBufferMemory to handle follow‑up questions.

🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

Please ensure code is well‑commented and follows PEP 8.

📄 License
Distributed under the MIT License. See LICENSE for more information.
