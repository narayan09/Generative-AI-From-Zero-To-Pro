# app.py (enhanced)
import streamlit as st
from text_to_sql import TextToSQL
from rag_retriever import RAGRetriever
import os
import tempfile
from ingest_documents import load_documents, chunk_text, get_embedding
import chromadb

st.set_page_config(page_title="Jira AI Assistant", layout="wide")
st.title("🎫 Jira AI Assistant")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "Database (SQL)"
if "show_uploader" not in st.session_state:
    st.session_state.show_uploader = False

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.radio(
        "Query Mode",
        ["Database (SQL)", "Document (RAG)"],
        index=0 if st.session_state.mode == "Database (SQL)" else 1
    )
    if mode != st.session_state.mode:
        st.session_state.mode = mode

    st.divider()
    st.subheader("📂 Manage Documents")
    if st.button("Upload / Re‑ingest Documents"):
        st.session_state.show_uploader = not st.session_state.show_uploader

    if st.session_state.show_uploader:
        uploaded_files = st.file_uploader(
            "Upload .txt, .md, or .pdf files",
            type=["txt", "md", "pdf"],
            accept_multiple_files=True
        )
        if uploaded_files:
            # Save to documents/ folder
            save_dir = "documents"
            os.makedirs(save_dir, exist_ok=True)
            for file in uploaded_files:
                file_path = os.path.join(save_dir, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
            st.success(f"Saved {len(uploaded_files)} file(s).")
            # Trigger re‑ingestion
            with st.spinner("Re‑ingesting all documents..."):
                # Re‑use the ingest logic
                try:
                    chroma_client = chromadb.PersistentClient(path="chroma_db")
                    collection = chroma_client.get_or_create_collection(
                        name="jira_docs",
                        metadata={"hnsw:space": "cosine"}
                    )
                    # Load all docs in folder
                    docs = load_documents(save_dir)
                    for filepath, content in docs:
                        chunks = chunk_text(content)
                        ids = [f"{os.path.basename(filepath)}_{i}" for i in range(len(chunks))]
                        embeddings = [get_embedding(chunk) for chunk in chunks]
                        collection.upsert(
                            ids=ids,
                            embeddings=embeddings,
                            metadatas=[{"source": filepath, "chunk": i} for i in range(len(chunks))],
                            documents=chunks
                        )
                    st.success(f"Ingested {collection.count()} chunks total.")
                    # Clear RAG engine cache so it picks up new docs
                    get_rag_engine.clear()
                except Exception as e:
                    st.error(f"Ingestion error: {e}")

    st.divider()
    st.caption("Database: natural language → SQL → results")
    st.caption("Document: search your uploaded files for answers")

# Cached engines
@st.cache_resource
def get_sql_engine():
    return TextToSQL()

@st.cache_resource
def get_rag_engine():
    return RAGRetriever()

sql_engine = get_sql_engine()
rag_engine = get_rag_engine()

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sql"):
            with st.expander("🔍 View SQL"):
                st.code(msg["sql"], language="sql")
        if msg.get("data") is not None and not msg["data"].empty:
            st.dataframe(msg["data"], use_container_width=True)

# Input
if prompt := st.chat_input("Ask me anything about Jira..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if st.session_state.mode == "Database (SQL)":
            with st.spinner("🤖 Thinking (SQL)..."):
                result = sql_engine.ask(prompt)
            if result["error"]:
                st.error(f"❌ {result['error']}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Error: {result['error']}",
                    "sql": None,
                    "data": None
                })
            else:
                sql = result["sql"]
                df = result["data"]
                if df.empty:
                    answer = "The query returned no rows."
                else:
                    answer = f"📊 Query returned {len(df)} row(s)."
                st.markdown(answer)
                if sql:
                    with st.expander("🔍 View generated SQL"):
                        st.code(sql, language="sql")
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sql": sql,
                    "data": df if not df.empty else None
                })
        else:
            with st.spinner("📚 Searching documents..."):
                answer, sources = rag_engine.generate_answer(prompt)
            st.markdown(answer)
            if sources:
                with st.expander("📄 Source chunks"):
                    for i, chunk in enumerate(sources):
                        st.markdown(f"**Chunk {i+1}:** {chunk[:400]}...")
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sql": None,
                "data": None
            })