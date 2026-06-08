from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama


loader = PyPDFLoader(
    "docs/building-blocks-of-rag-ebook-final.pdf"
)

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

# print(f"Loaded {len(docs)} pages")
# print(f"Split into {len(chunks)} ")
embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)
#print(f"Embedding chunks... {embedding}...")
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="./db"
)
print("Vector store created and persisted to disk.")

retriever = vector_db.as_retriever(
    search_kwargs={"k":3}
)

docs = retriever.invoke(
    "What is retrieval-augmented generation??"
)
llm = ChatOllama(
    model="qwen2.5:3b"
)

response = llm.invoke("What is retrieval-augmented generation?")
print(f"Response: {response}")