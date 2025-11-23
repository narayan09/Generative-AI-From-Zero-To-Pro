# 🚀 FastAPI + Ollama Backend

This backend provides:
- Token-based authentication  
- Token generation from Swagger UI  
- Secure API that sends prompts to the Ollama LLM  
- Works with the Streamlit frontend

---
## uvicorn app:app --reload

## 📁 Project Structure

app.py

🧪 Example Request (Swagger UI)
{
  "prompt": "Write a detailed explanation of AI.",
  "model": "llama3",
  "token_limit": 50
}

# 🚀 LangChain + OpenRouter LLM Chat Application

## 📋 Project Overview

This is a **full-stack LLM application** that combines **FastAPI backend** with **Streamlit frontend** to practice and master LangChain concepts using **OpenRouter APIs**. The project demonstrates real-world implementation of LLM integration, authentication, and multi-model support.

**What You're Building:**
- A secure chat application with **token-based authentication**
- Support for **multiple LLM models** (GPT-4, Claude, Gemini, Llama, Mistral) via OpenRouter
- Alternative **local LLM support** with Ollama
- **Frontend UI** for user interactions
- **Backend API** with protected routes
- **LangSmith integration** for monitoring and debugging LLM calls

---

## 🎯 Learning Outcomes

After completing this project, you will understand:

### Core LangChain Concepts
✅ **LLM Initialization** - Connecting to OpenRouter and configuring ChatOpenAI  
✅ **Model Configuration** - Working with different models and temperature settings  
✅ **LLM Invocation** - Basic model calls and response handling  
✅ **LangSmith Integration** - Tracing and monitoring LLM calls for debugging  

### Backend Development (FastAPI)
✅ **API Routing** - Creating modular endpoints with APIRouter  
✅ **Authentication** - Implementing token-based security with HTTPBearer  
✅ **Dependency Injection** - Using FastAPI dependencies for protecting routes  
✅ **Error Handling** - Proper HTTP exception handling and status codes  
✅ **Request/Response Management** - Structuring API communication  

### Frontend Development (Streamlit)
✅ **Session State Management** - Handling user tokens and data persistence  
✅ **Multi-tab UI** - Creating organized interface with tabs  
✅ **API Integration** - Making HTTP requests to backend from frontend  
✅ **User Input Handling** - Text input, buttons, and form submission  
✅ **Error Display** - User-friendly error messages and success notifications  

### DevOps & Configuration
✅ **Environment Variables** - Secure API key management with .env files  
✅ **Model Switching** - Supporting multiple LLM providers in one application  
✅ **Request/Response Handling** - Token limits, prompt configuration  

---

## 📁 Project Structure

```
project/
├── app.py                 # FastAPI main application & Ollama endpoint
├── open_router.py         # OpenRouter integration & LangChain config
├── auth.py                # Token generation & verification
├── llm_service.py         # LLM service with LangSmith tracing
├── langsmith_client.py    # LangSmith configuration (placeholder)
├── streamlit_app.py       # Streamlit frontend
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## 🔧 How Each File Works

### **1. `app.py` (FastAPI Backend)**
**Purpose:** Main backend server with protected routes

**Key Features:**
- `POST /generate-token` - Generate secure JWT-like tokens
- `POST /ask-ollama` - Protected route for Ollama model queries
- `POST /ask_prompt` - Protected route for OpenRouter queries (from open_router.py)
- Token verification using dependencies

**What You Learn:**
- FastAPI routing and dependency injection
- Token-based authentication pattern
- How to modularize routes using APIRouter

```python
# Example: Token generation and verification
@app.post("/generate-token")
def generate_token():
    token = secrets.token_hex(32)
    set_token(token)
    return {"token": token}

# Protected route - requires valid token
@app.post("/ask-ollama")
def ask_ollama(request: dict, _: bool = Depends(verify_token)):
    # Only accessible with valid token
```

---

### **2. `open_router.py` (LangChain + OpenRouter)**
**Purpose:** LangChain integration with OpenRouter for multi-model support

**Key Features:**
- `OpenRouterConfig` class with model dictionary
- `get_model()` method for LLM initialization
- `@router.post("/ask_prompt")` endpoint for OpenRouter queries
- LangSmith tracing with `@traceable` decorator

**What You Learn:**
- LangChain ChatOpenAI initialization with custom base URL
- Environment variable management for API keys
- Multi-model support (GPT-4, Claude, Gemini, Llama, Mistral)
- LangSmith tracing for debugging LLM calls

```python
# LangChain + OpenRouter integration
llm = ChatOpenAI(
    model="openai/gpt-4-turbo",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7
)
response = llm.invoke(prompt)
```

**Available Models:**
- `gpt-4` → openai/gpt-4-turbo
- `gpt-3.5` → openai/gpt-3.5-turbo
- `claude-3` → anthropic/claude-3-sonnet
- `claude-3.5` → anthropic/claude-3.5-sonnet
- `gemini` → google/gemini-pro
- `llama-3` → meta-llama/llama-3-70b-instruct
- `mistral` → mistralai/mistral-7b-instruct
- `grok-4.1` (default free model)

---

### **3. `auth.py` (Authentication)**
**Purpose:** Token generation and verification logic

**Key Features:**
- `set_token()` - Store generated token globally
- `verify_token()` - Dependency for protected routes
- HTTPBearer security scheme

**What You Learn:**
- How to implement token-based authentication
- FastAPI security dependencies
- Dependency injection pattern for route protection

```python
# How verification works
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != CURRENT_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True
```

---

### **4. `llm_service.py` (LLM Service with Tracing)**
**Purpose:** Service layer for LLM calls with LangSmith integration

**Key Features:**
- `@traceable` decorator for LangSmith monitoring
- Direct Ollama API integration
- Response parsing

**What You Learn:**
- LangSmith tracing for production monitoring
- Service layer architecture
- Direct HTTP calls to LLM providers

```python
@traceable  # Enables LangSmith tracing
def generate_llm_response(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={"model": "llama3", "prompt": prompt}
    )
    return response.json().get("response", "No response")
```

---

### **5. `streamlit_app.py` (Frontend UI)**
**Purpose:** Interactive user interface for the chat application

**Key Features:**
- **Tab 1: Ollama Chat**
  - Token generation/input
  - Token limit configuration
  - Chat input with LLM response
  
- **Tab 2: API Search**
  - OpenRouter-based search functionality
  - Same token authentication

**What You Learn:**
- Streamlit session state management
- Multi-tab UI organization
- HTTP request handling from frontend
- Error handling and user feedback

```python
# Session state for persistence
if "api_token" not in st.session_state:
    st.session_state.api_token = ""

# Tab-based UI
tab1, tab2 = st.tabs(["🧠 Ollama Chat", "🔎 API Search"])

# Protected API calls
if st.button("Send to LLM"):
    response = requests.post(
        f"{FASTAPI_URL}/ask-ollama",
        json={"prompt": prompt, "token_limit": token_limit},
        headers={"Authorization": f"Bearer {st.session_state.api_token}"}
    )
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenRouter API key (free tier available)
- Ollama installed (optional, for local LLM)

### Installation

1. **Clone or download the project files**

2. **Create `.env` file in project root:**
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here (optional)
```

3. **Install dependencies:**
```bash
pip install fastapi uvicorn streamlit langchain langchain-openai python-dotenv langsmith ollama requests
```

4. **Run FastAPI backend:**
```bash
python -m uvicorn app:app --reload
# Backend runs at http://localhost:8000
```

5. **Run Streamlit frontend (in new terminal):**
```bash
streamlit run streamlit_app.py
# Frontend opens at http://localhost:8501
```

---

## 🎓 LangChain Concepts Practiced

| Concept | File | Implementation |
|---------|------|-----------------|
| **LLM Initialization** | `open_router.py` | ChatOpenAI with OpenRouter base URL |
| **Model Configuration** | `open_router.py` | Temperature, model selection, headers |
| **LLM Invocation** | `open_router.py` | `llm.invoke(prompt)` |
| **LangSmith Tracing** | `llm_service.py` | `@traceable` decorator |
| **Error Handling** | `app.py`, `open_router.py` | HTTPException, try-catch blocks |
| **API Integration** | `streamlit_app.py` | requests library for backend calls |

---

## 📚 Next Steps & Improvements

### Phase 2 - Advanced LangChain Concepts:
- ✅ Add **Memory** - ConversationBufferMemory for chat history
- ✅ Implement **Chains** - SequentialChain for multi-step prompts
- ✅ Create **Agents** - React agents with tool use
- ✅ Build **RAG** - Retrieval-Augmented Generation with ChromaDB
- ✅ Add **Prompts** - PromptTemplate for structured prompts

### Phase 3 - Production Ready:
- ✅ Database integration (PostgreSQL for user management)
- ✅ Real JWT tokens instead of simple secrets
- ✅ Rate limiting on API endpoints
- ✅ Docker containerization
- ✅ CI/CD deployment (GitHub Actions)

---

## 💡 Tips for Learning

1. **Start with the Frontend** - Run `streamlit run streamlit_app.py` to see the UI
2. **Generate a Token** - Click "Generate Token" to get started
3. **Experiment with Models** - Try different models in `open_router.py`
4. **Monitor with LangSmith** - Add your LANGSMITH_API_KEY to trace calls
5. **Add Your Own Endpoints** - Create new routes following the pattern
6. **Check Backend Logs** - Terminal shows FastAPI request/response logs

---

## 🔗 Resources

- **LangChain Docs:** https://python.langchain.com
- **OpenRouter API:** https://openrouter.ai/docs
- **FastAPI:** https://fastapi.tiangolo.com
- **Streamlit:** https://streamlit.io
- **LangSmith:** https://smith.langchain.com

---

## 📝 License

This is a practice/educational project. Feel free to modify and use for learning!

---

## ❓ Troubleshooting

**Q: "Invalid token" error**  
A: Click "Generate Token" first before sending prompts.

**Q: OpenRouter API key not working**  
A: Check `.env` file has `OPENROUTER_API_KEY` and it's correctly set.

**Q: Ollama endpoint not found**  
A: Ensure Ollama is running (`ollama serve`) before testing Ollama routes.

**Q: Streamlit can't connect to backend**  
A: Check FastAPI is running on `http://127.0.0.1:8000`

---

**Happy Learning! 🚀 Master LangChain by building real applications!**
