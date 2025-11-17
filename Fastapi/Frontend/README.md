# 🖥️ Streamlit Frontend for FastAPI + Ollama

This Streamlit app provides a simple UI to interact with your FastAPI backend.  
It allows users to:

✅ Generate a token from the backend  
✅ Save the token in session state  
✅ Send prompts to the LLM (via backend `/ask-ollama` route)  
✅ Show LLM responses in real time  

---

# 📁 Project Structure

frontend/
│── app.py # Streamlit UI
└── README.md

---

# ⚙️ How the Frontend Works

## 🔐 1. Token Generation Logic

When the user clicks “Generate Token”:

- Streamlit sends a **POST request** to:
on the backend.

- Backend returns a token:

{
  "token": "a94fc...99bb"
}


## streamlit run app.py
## How to Use the Frontend
Step 1 — Generate Token

    Click the "Generate Token" button
    Your token will appear in a success message
    Token is saved automatically in session state

Step 2 — Enter Your Prompt

Example:

Tell me a motivation quote 

Step 3 — Send to LLM

Click "Send to LLM"
You will see an AI response from Ollama backend