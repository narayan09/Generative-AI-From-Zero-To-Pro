import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="RAG Q&A", layout="wide")

st.title("📚 RAG Question Answering System")
st.write("Ask questions across TXT, PDF, and Database knowledge")

question = st.text_input("Ask a question")

source_filter = st.selectbox(
    "Filter by source (optional)",
    ["All", "txt", "pdf", "sqlite"]
)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question")
    else:
        params = {"question": question}
        if source_filter != "All":
            params["source_type"] = source_filter

        with st.spinner("Thinking..."):
            response = requests.get(API_URL, params=params).json()

        st.subheader("🧠 Answer")
        st.success(response["answer"])

        st.metric("Confidence", response["confidence"])

        st.subheader("📌 Sources")
        for src in response["sources"]:
            st.json(src)
