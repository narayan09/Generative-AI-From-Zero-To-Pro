import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000"  # Backend URL

st.set_page_config(page_title="LLM Chat App", layout="centered")

st.title("💬 LLM Chat App (FastAPI + Streamlit)")
st.write("Send messages to the LLM running in FastAPI/Ollama backend.")

# --- Token Section ---
st.subheader("🔐 Generate or Enter Token")

if "api_token" not in st.session_state:
    st.session_state.api_token = ""

# Input for existing token
token_input = st.text_input("Enter API Token", st.session_state.api_token)

# Button to generate token from backend
if st.button("Generate Token"):
    try:
        response = requests.post(f"{FASTAPI_URL}/generate-token")
        token = response.json().get("token")
        st.session_state.api_token = token
        st.success(f"Token generated: {token}")
    except Exception as e:
        st.error(f"Error generating token: {e}")

# --- Chat Section ---
st.subheader("💭 Ask the LLM")

prompt = st.text_area("Enter your prompt:")

if st.button("Send to LLM"):
    if not st.session_state.api_token:
        st.error("Please generate or enter a token first.")
    else:
        try:
            response = requests.post(
                f"{FASTAPI_URL}/ask-ollama",
                json={"prompt": prompt},
                headers={"Authorization": f"Bearer {st.session_state.api_token}"}
            )
            
            if response.status_code == 200:
                st.success("Response from LLM:")
                st.write(response.json()["response"])
            else:
                st.error(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Error calling backend: {e}")

