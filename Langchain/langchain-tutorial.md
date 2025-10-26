# LangChain: From Zero to Hero - Complete AI Engineer Tutorial

## Table of Contents
1. [Introduction to LangChain](#1-introduction-to-langchain)
2. [Environment Setup](#2-environment-setup)
3. [Core Concepts & Components](#3-core-concepts--components)
4. [LangChain Expression Language (LCEL)](#4-langchain-expression-language-lcel)
5. [Prompt Engineering with LangChain](#5-prompt-engineering-with-langchain)
6. [Memory & Conversation Management](#6-memory--conversation-management)
7. [Retrieval Augmented Generation (RAG)](#7-retrieval-augmented-generation-rag)
8. [Vector Databases & Embeddings](#8-vector-databases--embeddings)
9. [Agents & Tools](#9-agents--tools)
10. [LangGraph: State Management & Workflows](#10-langgraph-state-management--workflows)
11. [LangSmith: Observability & Debugging](#11-langsmith-observability--debugging)
12. [Production Deployment with LangServe](#12-production-deployment-with-langserve)
13. [Advanced Topics](#13-advanced-topics)
14. [Best Practices & Security](#14-best-practices--security)
15. [Real-World Projects](#15-real-world-projects)

---

## 1. Introduction to LangChain

### What is LangChain?
LangChain is an open-source framework designed to simplify the development of applications powered by Large Language Models (LLMs). It provides a modular architecture that enables developers to build context-aware, production-ready AI applications efficiently.

### Why LangChain?
- **Modular Components**: Reusable building blocks for prompts, models, chains, and agents
- **Framework Agnostic**: Works with OpenAI, Anthropic, Google, Hugging Face, and more
- **Production Ready**: Built-in observability, streaming, and deployment capabilities
- **Community Driven**: Extensive integrations and active development

### Key Features
- Prompt management and templating
- Chain composition for multi-step workflows
- Memory management for conversational context
- RAG (Retrieval Augmented Generation) support
- Agent framework with tool integration
- Streaming and async support
- LangSmith integration for monitoring

---

## 2. Environment Setup

### Installation

```bash
# Core LangChain package
pip install langchain

# LangChain Community integrations
pip install langchain-community

# LangChain Core (minimal dependencies)
pip install langchain-core

# Specific LLM providers
pip install langchain-openai        # For OpenAI
pip install langchain-anthropic     # For Claude
pip install langchain-google-genai  # For Google Gemini

# For 100% Local & Private (No Internet After Setup):
- LLM: Ollama with Llama 3.1 or Mistral
- Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
- Vector DB: Chroma (persistent) or FAISS (fast)
- Monitoring: Skip LangSmith or use free tier

# For Best Performance (Minimal APIs):

- LLM: Ollama locally OR Hugging Face API (free tier)
- Embeddings: Sentence Transformers (local)
- Vector DB: Chroma or FAISS (local)
- Monitoring: LangSmith free tier (5k traces/month)

# For RAG and vector databases
pip install langchain-chroma
pip install faiss-cpu
pip install sentence-transformers

# For deployment
pip install langserve
pip install fastapi
pip install uvicorn

# For observability
pip install langsmith
```

### Environment Variables

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = "your-api-key"
os.environ["ANTHROPIC_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-key"
os.environ["LANGCHAIN_TRACING_V2"] = "true"  # Enable LangSmith tracing
```

### First LangChain Program

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Initialize the model
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Create a message
messages = [HumanMessage(content="What is LangChain?")]

# Get response
response = llm.invoke(messages)
print(response.content)
```

---

## 3. Core Concepts & Components

### 3.1 Schema & Data Structures

LangChain uses standardized data structures for consistency[65]:

```python
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

# Message types
system_msg = SystemMessage(content="You are a helpful assistant")
human_msg = HumanMessage(content="Hello, how are you?")
ai_msg = AIMessage(content="I'm doing well, thank you!")
```

### 3.2 Models

LangChain supports multiple model types[18]:

#### Chat Models
```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# OpenAI
openai_chat = ChatOpenAI(model="gpt-4", temperature=0.7)

# Anthropic Claude
claude_chat = ChatAnthropic(model="claude-3-sonnet-20240229")
```

#### LLMs (Text Completion)
```python
from langchain_openai import OpenAI

llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.7)
response = llm.invoke("Write a haiku about programming")
```

#### Embeddings
```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectors = embeddings.embed_documents(["Hello world", "LangChain is great"])
```

### 3.3 Prompt Templates

Create reusable, dynamic prompts[18]:

```python
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# Simple prompt template
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?"
)

# Chat prompt template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant specialized in {domain}"),
    ("human", "{question}")
])

# Use the template
formatted = chat_prompt.format_messages(
    domain="data science",
    question="What is machine learning?"
)
```

### 3.4 Output Parsers

Structure LLM outputs into usable formats[18]:

```python
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

# String parser
str_parser = StrOutputParser()

# JSON parser with Pydantic
class ProductReview(BaseModel):
    product: str = Field(description="The product name")
    rating: int = Field(description="Rating from 1-5")
    summary: str = Field(description="Brief summary")

json_parser = JsonOutputParser(pydantic_object=ProductReview)

# Use in a chain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
chain = llm | json_parser

result = chain.invoke("Review: iPhone 15 - Great phone! 5 stars")
```

### 3.5 Chains

Chains combine multiple components into workflows[53]:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Create components
model = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
parser = StrOutputParser()

# Create chain using pipe operator
chain = prompt | model | parser

# Invoke the chain
result = chain.invoke({"topic": "programming"})
print(result)
```

---

## 4. LangChain Expression Language (LCEL)

LCEL is a declarative syntax for building chains with optimized execution[54][60][63].

### Benefits of LCEL
- **Optimized parallel execution**: Automatic parallelization where possible
- **Guaranteed async support**: All chains support async by default
- **Streaming**: Incremental output as it's generated
- **Seamless LangSmith tracing**: Automatic logging for debugging
- **Deployable with LangServe**: One-click deployment

### Basic LCEL Syntax

The pipe operator (`|`) chains components together[54]:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
output_parser = StrOutputParser()

# Chain using LCEL
chain = prompt | llm | output_parser

# Invoke
result = chain.invoke({"topic": "quantum computing"})
```

### Runnables

Everything in LCEL implements the `Runnable` interface[60]:

```python
# Invoke (synchronous)
result = chain.invoke({"topic": "AI"})

# Batch processing
results = chain.batch([
    {"topic": "AI"},
    {"topic": "ML"},
    {"topic": "DL"}
])

# Stream output
for chunk in chain.stream({"topic": "blockchain"}):
    print(chunk, end="", flush=True)

# Async invoke
import asyncio
result = await chain.ainvoke({"topic": "async programming"})
```

### Parallel Execution with RunnableParallel

```python
from langchain_core.runnables import RunnableParallel

# Define parallel tasks
parallel_chain = RunnableParallel({
    "joke": prompt | llm | StrOutputParser(),
    "poem": ChatPromptTemplate.from_template("Write a poem about {topic}") 
            | llm | StrOutputParser()
})

# Execute in parallel
results = parallel_chain.invoke({"topic": "programming"})
print(results["joke"])
print(results["poem"])
```

### RunnablePassthrough

Pass data through unchanged or extract specific keys[57]:

```python
from langchain_core.runnables import RunnablePassthrough

chain = (
    RunnablePassthrough.assign(
        # Add new fields while preserving original
        enhanced=lambda x: x["original"].upper()
    )
    | prompt
    | llm
)
```

---

## 5. Prompt Engineering with LangChain

### Few-Shot Prompting

```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

# Define examples
examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "hot", "output": "cold"}
]

# Example template
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}"
)

# Few-shot prompt
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Give the antonym of the word:",
    suffix="Input: {word}\nOutput:",
    input_variables=["word"]
)

chain = few_shot_prompt | llm | StrOutputParser()
result = chain.invoke({"word": "fast"})
```

### Prompt Templates with Multiple Variables

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} specializing in {domain}"),
    ("human", "Question: {question}\nContext: {context}"),
])

chain = prompt | llm | StrOutputParser()

result = chain.invoke({
    "role": "data scientist",
    "domain": "machine learning",
    "question": "What is overfitting?",
    "context": "Discussing model training issues"
})
```

### Partial Prompts

```python
# Set some variables ahead of time
partial_prompt = prompt.partial(
    role="software engineer",
    domain="system design"
)

# Later, provide remaining variables
result = partial_prompt.invoke({
    "question": "How to design a scalable API?",
    "context": "Building a microservices architecture"
})
```

---

## 6. Memory & Conversation Management

LangChain provides multiple memory types for maintaining conversational context[55][58][61].

### 6.1 ConversationBufferMemory

Stores all messages in a buffer[58]:

```python
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

memory = ConversationBufferMemory(return_messages=True)

llm = ChatOpenAI(model="gpt-4")
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# First interaction
response1 = conversation.invoke("Hi, my name is Alice")
# Second interaction - remembers name
response2 = conversation.invoke("What's my name?")
```

### 6.2 ConversationBufferWindowMemory

Keeps only the last K interactions[55]:

```python
from langchain.memory import ConversationBufferWindowMemory

# Keep only last 3 messages
memory = ConversationBufferWindowMemory(
    k=3,
    return_messages=True
)

conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

### 6.3 ConversationSummaryMemory

Summarizes conversation history[61]:

```python
from langchain.memory import ConversationSummaryMemory

memory = ConversationSummaryMemory(
    llm=llm,
    return_messages=True
)

conversation = ConversationChain(
    llm=llm,
    memory=memory
)
```

### 6.4 ConversationSummaryBufferMemory

Combines summary and buffer approaches[55]:

```python
from langchain.memory import ConversationSummaryBufferMemory

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=100,
    return_messages=True
)
```

### Modern Approach: RunnableWithMessageHistory

The recommended approach for managing conversational memory[61][64]:

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Store for different sessions
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Create chain with memory
chain = prompt | llm

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Use with session ID
config = {"configurable": {"session_id": "user_123"}}
response = chain_with_history.invoke(
    {"input": "Hi, I'm Alice"},
    config=config
)
```

---

## 7. Retrieval Augmented Generation (RAG)

RAG enhances LLMs by retrieving relevant information from external knowledge bases[73][74][90][93].

### Why RAG?
- Reduces hallucinations
- Incorporates up-to-date information
- Enables domain-specific knowledge
- Provides source attribution

### Basic RAG Pipeline

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Load documents
loader = TextLoader("data.txt")
documents = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)

# 3. Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 4. Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 5. Create RAG chain
llm = ChatOpenAI(model="gpt-4")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# Query
result = qa_chain.invoke({"query": "What is LangChain?"})
print(result["result"])
print(result["source_documents"])
```

### Modern RAG with LCEL

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# RAG prompt
rag_prompt = ChatPromptTemplate.from_template("""
Use the following context to answer the question.

Context: {context}

Question: {question}

Answer:
""")

# Format documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG chain with LCEL
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | rag_prompt
    | llm
    | StrOutputParser()
)

# Query
result = rag_chain.invoke("What is machine learning?")
```

### Advanced RAG: Parent Document Retriever

Retrieves smaller chunks but uses larger context[96]:

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

# Storage for parent documents
store = InMemoryStore()

# Child splitter (smaller chunks for retrieval)
child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50
)

# Parent splitter (larger chunks for context)
parent_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200
)

# Create retriever
parent_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)

# Add documents
parent_retriever.add_documents(documents)
```

---

## 8. Vector Databases & Embeddings

Vector databases enable semantic search for RAG applications[92][95][98].

### Supported Vector Stores
- FAISS (local, in-memory)
- Chroma (local, persistent)
- Pinecone (cloud-hosted)
- Weaviate (self-hosted or cloud)
- Qdrant (self-hosted or cloud)
- Milvus (self-hosted or cloud)

### Working with Embeddings

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Embed documents
docs = ["Hello world", "LangChain is amazing", "Vector databases are powerful"]
doc_vectors = embeddings.embed_documents(docs)

# Embed query
query = "What is LangChain?"
query_vector = embeddings.embed_query(query)
```

### FAISS Vector Store

```python
from langchain_community.vectorstores import FAISS

# Create from documents
vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

# Save locally
vectorstore.save_local("faiss_index")

# Load from disk
loaded_vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# Search
results = vectorstore.similarity_search("machine learning", k=3)
```

### Chroma Vector Store

```python
from langchain_community.vectorstores import Chroma

# Create persistent store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Load existing store
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
```

### Advanced Retrieval Methods

```python
# Similarity search with scores
results = vectorstore.similarity_search_with_score("AI", k=3)
for doc, score in results:
    print(f"Score: {score}, Content: {doc.page_content[:100]}")

# Max Marginal Relevance (MMR) - diversity
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 10}
)

# Similarity threshold
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.8}
)
```

---

## 9. Agents & Tools

Agents use LLMs to decide which tools to use and when[91][94][97][100].

### What are Agents?
Agents are systems where LLMs dynamically determine the sequence of actions based on user input. They can:
- Reason about which tool to use
- Execute tools in sequence
- Adapt based on tool outputs

### Creating Tools

```python
from langchain.tools import tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Custom tool using decorator
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information."""
    api_wrapper = WikipediaAPIWrapper()
    return api_wrapper.run(query)

# Pre-built tools
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
```

### Building a ReAct Agent

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub

# Pull a prompt from LangChain Hub
prompt = hub.pull("hwchase17/react")

# Create tools
tools = [multiply, search_wikipedia]

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create agent
agent = create_react_agent(llm, tools, prompt)

# Create executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# Run agent
result = agent_executor.invoke({
    "input": "What is the population of France multiplied by 2?"
})
```

### OpenAI Functions Agent

```python
from langchain.agents import create_openai_functions_agent

agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)
```

### Tool Selection with LangGraph

For complex tool routing, LangGraph provides more control[91]:

```python
from langgraph.prebuilt import create_react_agent

tools = [multiply, search_wikipedia]

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet",
    tools=tools
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What's 42 x 7?"}]
})
```

---

## 10. LangGraph: State Management & Workflows

LangGraph is a framework for building stateful, multi-agent applications with LangChain[141][142][157][160].

### Why LangGraph?
- **State Management**: Maintain complex state across interactions
- **Cyclic Workflows**: Build agents that can loop and iterate
- **Human-in-the-Loop**: Add approval steps and interventions
- **Persistence**: Save and resume agent state
- **Multi-Agent Systems**: Coordinate multiple agents

### Core Concepts

1. **State**: The data structure passed between nodes
2. **Nodes**: Functions that process state
3. **Edges**: Connections between nodes
4. **Conditional Edges**: Dynamic routing based on state

### Basic LangGraph Example

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_openai import ChatOpenAI

# Define state
class AgentState(TypedDict):
    messages: list
    next_action: str

# Define nodes
def call_model(state: AgentState):
    llm = ChatOpenAI()
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState):
    # Decide next step based on state
    if state["messages"][-1].content.endswith("?"):
        return "call_model"
    return END

# Build graph
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("agent", call_model)

# Add edges
builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    should_continue,
    {"call_model": "agent", END: END}
)

# Compile
graph = builder.compile()

# Run
result = graph.invoke({
    "messages": [{"role": "user", "content": "Hello!"}]
})
```

### Agent with Tools and State

```python
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    return f"The weather in {location} is sunny, 25°C"

# Use MessagesState (built-in)
def should_continue(state: MessagesState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

def call_model(state: MessagesState):
    llm = ChatOpenAI(model="gpt-4")
    model_with_tools = llm.bind_tools([get_weather])
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode([get_weather]))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")

graph = builder.compile()

# Run
result = graph.invoke({
    "messages": [{"role": "user", "content": "What's the weather in Paris?"}]
})
```

### Persistence with Checkpointers

```python
from langgraph.checkpoint.memory import MemorySaver

# Add memory
checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Use with thread ID for persistence
config = {"configurable": {"thread_id": "conversation-1"}}

# First interaction
result1 = graph.invoke(
    {"messages": [{"role": "user", "content": "Hi, I'm Alice"}]},
    config=config
)

# Second interaction - remembers previous
result2 = graph.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    config=config
)
```

---

## 11. LangSmith: Observability & Debugging

LangSmith provides tracing, monitoring, and debugging for LangChain applications[122][125][128][131][134].

### Why LangSmith?
- **Complete Tracing**: See every step of chain execution
- **Debugging**: Identify failures and bottlenecks
- **Monitoring**: Track costs, latency, and quality
- **Evaluation**: Test and compare chain variations
- **Production Analytics**: Monitor real-world usage

### Setup LangSmith

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"
```

### Automatic Tracing

Once configured, all LangChain operations are automatically traced:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")

chain = prompt | llm

# This will automatically log to LangSmith
result = chain.invoke({"topic": "quantum computing"})
```

### Custom Tags and Metadata

```python
# Add tags for filtering
result = chain.invoke(
    {"topic": "AI"},
    config={
        "tags": ["production", "v1.0"],
        "metadata": {"user_id": "123", "session": "abc"}
    }
)
```

### Callbacks for Custom Tracking

```python
from langchain.callbacks import get_openai_callback

# Track token usage and costs
with get_openai_callback() as cb:
    result = chain.invoke({"topic": "blockchain"})
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Total Cost: ${cb.total_cost:.4f}")
```

### Evaluation with LangSmith

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Define evaluator
def is_helpful(run, example):
    # Custom evaluation logic
    score = 1 if len(run.outputs["output"]) > 100 else 0
    return {"score": score}

# Run evaluation
results = evaluate(
    lambda inputs: chain.invoke(inputs),
    data="my-dataset",
    evaluators=[is_helpful],
    experiment_prefix="helpful-test"
)
```

---

## 12. Production Deployment with LangServe

LangServe enables easy deployment of LangChain applications as REST APIs[121][124][127][130].

### Why LangServe?
- **FastAPI Integration**: Production-ready web server
- **Auto-generated Docs**: Swagger UI for your chains
- **Streaming Support**: Real-time token streaming
- **Batch Processing**: Handle multiple requests efficiently
- **Playground UI**: Test your API interactively

### Basic Deployment

**1. Create your chain** (`chain.py`):

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
output_parser = StrOutputParser()

chain = prompt | llm | output_parser
```

**2. Create server** (`server.py`):

```python
from fastapi import FastAPI
from langserve import add_routes
from chain import chain

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces"
)

# Add chain routes
add_routes(
    app,
    chain,
    path="/joke"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**3. Run the server**:

```bash
python server.py
```

### API Endpoints

LangServe automatically creates:
- `/joke/invoke` - Single request
- `/joke/batch` - Multiple requests
- `/joke/stream` - Streaming response
- `/joke/playground` - Interactive testing UI
- `/docs` - Swagger documentation

### Client Usage

```python
from langserve import RemoteRunnable

# Connect to deployed chain
remote_chain = RemoteRunnable("http://localhost:8000/joke/")

# Invoke
result = remote_chain.invoke({"topic": "programming"})

# Stream
for chunk in remote_chain.stream({"topic": "AI"}):
    print(chunk, end="", flush=True)

# Batch
results = remote_chain.batch([
    {"topic": "data science"},
    {"topic": "cloud computing"}
])
```

### Multiple Chains

```python
from fastapi import FastAPI
from langserve import add_routes

app = FastAPI()

# Add multiple chains
add_routes(app, joke_chain, path="/joke")
add_routes(app, summary_chain, path="/summarize")
add_routes(app, qa_chain, path="/qa")
```

### Deployment to Cloud

**Docker**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Google Cloud Run**:

```bash
gcloud run deploy langchain-api \
    --source . \
    --region us-central1 \
    --allow-unauthenticated
```

---

## 13. Advanced Topics

### 13.1 Fine-Tuning with LangChain

While LangChain focuses on prompt engineering and RAG, you can integrate fine-tuned models[123][126]:

```python
from langchain_openai import ChatOpenAI

# Use your fine-tuned model
fine_tuned_llm = ChatOpenAI(
    model="ft:gpt-3.5-turbo:my-org:custom_suffix:id",
    temperature=0.7
)

chain = prompt | fine_tuned_llm | output_parser
```

### 13.2 Multi-Modal Applications

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4-vision-preview")

# Image input
message = HumanMessage(
    content=[
        {"type": "text", "text": "What's in this image?"},
        {
            "type": "image_url",
            "image_url": {"url": "https://example.com/image.jpg"}
        }
    ]
)

response = llm.invoke([message])
```

### 13.3 Structured Output

Force LLMs to return JSON or specific formats:

```python
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age")
    occupation: str = Field(description="Person's job")

llm = ChatOpenAI(model="gpt-4")

# Structured output
structured_llm = llm.with_structured_output(Person)

result = structured_llm.invoke("Tell me about John, a 30-year-old engineer")
print(result.name, result.age, result.occupation)
```

### 13.4 Caching

Reduce costs and latency by caching LLM responses:

```python
from langchain.cache import SQLiteCache
from langchain.globals import set_llm_cache

# Enable caching
set_llm_cache(SQLiteCache(database_path=".langchain.db"))

# Subsequent identical calls will use cache
chain = prompt | llm | output_parser
result = chain.invoke({"topic": "AI"})  # Cached on second call
```

### 13.5 Async and Concurrency

```python
import asyncio
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

async def process_multiple():
    tasks = [
        llm.ainvoke("Tell me about Python"),
        llm.ainvoke("Tell me about JavaScript"),
        llm.ainvoke("Tell me about Rust")
    ]
    results = await asyncio.gather(*tasks)
    return results

# Run async
results = asyncio.run(process_multiple())
```

---

## 14. Best Practices & Security

### 14.1 Security Best Practices[158][161][164][169]

**Input Validation**:
```python
def sanitize_input(user_input: str) -> str:
    # Remove dangerous characters
    dangerous_patterns = ["<script>", "'; DROP TABLE", "exec("]
    for pattern in dangerous_patterns:
        if pattern in user_input.lower():
            raise ValueError("Invalid input detected")
    return user_input
```

**API Key Management**:
```python
import os
from dotenv import load_dotenv

# Never hardcode keys
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Use environment variables
llm = ChatOpenAI(openai_api_key=api_key)
```

**Rate Limiting**:
```python
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

@app.post("/chat")
@limiter.limit("10/minute")
async def chat_endpoint(request: Request):
    # Handle request
    pass
```

**Content Moderation**:
```python
from langchain_openai import OpenAI

def moderate_content(text: str) -> bool:
    # Use OpenAI moderation
    import openai
    response = openai.moderations.create(input=text)
    return not response.results[0].flagged

# Use in chain
if not moderate_content(user_input):
    raise ValueError("Content violates policy")
```

### 14.2 Production Best Practices

**Error Handling**:
```python
from langchain_core.runnables import RunnableLambda

def safe_invoke(chain, input_data, fallback_response="I'm having trouble"):
    try:
        return chain.invoke(input_data)
    except Exception as e:
        print(f"Error: {e}")
        return fallback_response
```

**Monitoring and Alerting**:
```python
from langchain.callbacks import get_openai_callback
import logging

logger = logging.getLogger(__name__)

with get_openai_callback() as cb:
    result = chain.invoke(input_data)
    
    # Log metrics
    logger.info(f"Tokens used: {cb.total_tokens}")
    
    # Alert on high costs
    if cb.total_cost > 0.10:
        logger.warning(f"High cost detected: ${cb.total_cost}")
```

**Graceful Degradation**:
```python
from langchain.schema.runnable import RunnableWithFallbacks

# Primary chain
primary_chain = prompt | gpt4_llm | parser

# Fallback chain (cheaper model)
fallback_chain = prompt | gpt35_llm | parser

# Chain with fallback
chain = primary_chain.with_fallbacks([fallback_chain])
```

---

## 15. Real-World Projects

### Project 1: Document Q&A System

```python
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load documents
loader = DirectoryLoader("./documents", glob="**/*.txt")
documents = loader.load()

# Split
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# RAG chain
template = """Answer based on context:

Context: {context}
Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(model="gpt-4")

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Query
answer = rag_chain.invoke("What is the main topic of the documents?")
```

### Project 2: Multi-Agent Research Assistant

```python
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from typing import TypedDict, List

class ResearchState(TypedDict):
    query: str
    search_results: List[str]
    summary: str

# Tools
search = DuckDuckGoSearchRun()
llm = ChatOpenAI(model="gpt-4")

# Nodes
def search_node(state: ResearchState):
    results = search.run(state["query"])
    return {"search_results": [results]}

def summarize_node(state: ResearchState):
    prompt = f"Summarize: {state['search_results']}"
    summary = llm.invoke(prompt).content
    return {"summary": summary}

# Build graph
builder = StateGraph(ResearchState)
builder.add_node("search", search_node)
builder.add_node("summarize", summarize_node)

builder.add_edge(START, "search")
builder.add_edge("search", "summarize")
builder.add_edge("summarize", END)

graph = builder.compile()

# Run
result = graph.invoke({"query": "Latest AI trends 2025"})
print(result["summary"])
```

### Project 3: Conversational RAG Chatbot

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Setup RAG
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

# Contextualize question
contextualize_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given chat history and latest question, formulate standalone question."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

# Answer question
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "Use context to answer:\n\n{context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])

llm = ChatOpenAI(model="gpt-4")

# Build chain
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Add memory
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversational_rag = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer"
)

# Use
config = {"configurable": {"session_id": "user123"}}
response = conversational_rag.invoke(
    {"input": "What is LangChain?"},
    config=config
)
```

---

## Summary

You've now covered everything you need to know to build production-ready AI applications with LangChain:

✅ **Foundations**: Setup, core concepts, and components  
✅ **LCEL**: Modern chain composition  
✅ **Prompt Engineering**: Effective LLM communication  
✅ **Memory**: Conversational context management  
✅ **RAG**: External knowledge integration  
✅ **Vector Databases**: Semantic search  
✅ **Agents**: Dynamic tool use  
✅ **LangGraph**: Complex workflows  
✅ **LangSmith**: Observability  
✅ **LangServe**: Production deployment  
✅ **Advanced**: Fine-tuning, security, best practices  
✅ **Projects**: Real-world implementations

## Next Steps

1. **Practice**: Build projects using the examples above
2. **Explore**: Check out [LangChain documentation](https://python.langchain.com/)
3. **Community**: Join [LangChain Discord](https://discord.gg/langchain)
4. **Stay Updated**: Follow [LangChain Blog](https://blog.langchain.dev)
5. **Contribute**: Submit issues or PRs to [LangChain GitHub](https://github.com/langchain-ai/langchain)

## Resources

- **Official Docs**: https://python.langchain.com/docs/
- **LangChain Hub**: https://smith.langchain.com/hub
- **LangSmith**: https://smith.langchain.com/
- **GitHub**: https://github.com/langchain-ai/langchain
- **YouTube Tutorials**: Search "LangChain tutorials 2025"
- **Courses**: DeepLearning.AI LangChain courses

---

**Happy Building! 🦜⛓️**
