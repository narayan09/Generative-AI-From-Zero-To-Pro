# MCP Roadmap (Interview + Practical)

## 5-Day MCP Learning Plan

### 🧩 Day 1 — Core Understanding (WHY MCP)

**Goal:** Understand problem MCP solves

**Learn:**
- Why APIs ≠ MCP
- Tool calling limitations in LangChain
- MCP architecture: Client, Server, Tools, Resources

**Task:**
Build a simple LLM + tool (without MCP) – e.g., ask “What’s weather in Pune?” and call API manually.

**Interview Focus:**
- Why MCP?
- Problems with direct tool integration

---

### 🔌 Day 2 — First MCP Server

**Goal:** Understand MCP structure

**Learn:**
- MCP server basics
- Tool schema (VERY IMPORTANT)
- JSON-RPC / structured interface

**Project:**
Build MCP server with:
- Tool 1: `get_weather(city)`
- Tool 2: `calculate(expression)`

Then connect via MCP client.

**Interview Focus:**
- What is an MCP server?
- How are tools exposed?

---

### ⚙️ Day 3 — Tool Orchestration

**Goal:** Let AI decide which tool to use

**Learn:**
- Tool selection logic
- Function calling vs MCP tools
- Structured outputs

**Project:**
Build AI assistant that takes input like “Plan my day in Mumbai weather” – AI calls weather tool, uses response, generates plan.

**Interview Focus:**
- How does LLM choose tools?
- Role of schema?

---

### 🧠 Day 4 — Advanced Concepts

**Goal:** Stand out in interview

**Learn:**
- Multi-tool systems
- Error handling
- Context passing
- Tool chaining

**Project:**
Build AI Research Assistant with tools: Search, Summarize, Save notes.

**Interview Focus:**
- Tool chaining
- Context management
- Limitations of MCP

---

### 🌐 Day 5 — Production + Mock Interview

**Goal:** Be interview ready

**Learn:**
- Scaling MCP
- Security basics
- Rate limiting
- Observability

**Final Project:**
Build Mini AI Agent with MCP tools – Chat UI, multiple tools, clean architecture.

**Interview Prep (VERY IMPORTANT):**
Prepare answers for:
1. What is MCP?
2. MCP vs API?
3. MCP vs LangChain tools?
4. How tool selection works?
5. Real-world use cases

---

## Practice Strategy

Each day:
- 2 hrs learning
- 2 hrs building
- 30 min explaining

---

## High‑Level Roadmap: 4 Phases to Mastery

| Phase | Focus | Key Concepts & Technologies | Hands‑on Project |
|-------|-------|-----------------------------|------------------|
| 1. Foundation | Understanding the why and what of MCP | Client‑Server Architecture, JSON‑RPC, Stdio & Streamable HTTP Transports, Tools, Resources, Prompts | Build a simple "Hello World" server with a single tool (e.g., calculator or weather fetcher) |
| 2. Core Skills | Building robust, functional servers with multiple capabilities | Structured Output, Error Handling, Multiple Tools/Resources, Testing with MCP Inspector | A "File System" server to read/write files, or a "Database Query" server to connect to a real database |
| 3. Advanced Skills | Designing and deploying production‑ready, secure servers | OAuth 2.1 Authorization, Advanced Transport (Streamable HTTP), Semantic Tool Routing, Deployment (e.g., Cloud Run, AWS) | A secure "Customer Data Platform" server with OAuth authentication, deployed to a cloud platform |
| 4. Expert Level | Mastering complex, interactive, and multi‑agent systems | Sampling, Elicitation, Asynchronous Tasks, Roots, Multi‑Agent Coordination | An "Intelligent Research Assistant" using Sampling for web search and Elicitation for user input, or a "Coordinator" for multi‑agent tasks |