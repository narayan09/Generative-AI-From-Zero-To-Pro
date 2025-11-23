import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000"  # Backend URL

st.set_page_config(page_title="LLM Chat App", layout="centered")

st.title("💬 LLM Chat App (FastAPI + Streamlit)")
st.write("This app communicates with the FastAPI backend.")

# ==================================================================
# TAB LAYOUT
# ==================================================================
tab1, tab2 = st.tabs(["🧠 Ollama Chat", "🔎 API Search"])

# -----------------------------------------------------------
# ===========================================================
# TAB 1 - OLLAMA (Your existing UI)
# ===========================================================
# -----------------------------------------------------------
with tab1:

    st.header("🧠 Ollama Chat")

    # --- Token Section ---
    st.subheader("🔐 Generate or Enter Token")

    if "api_token" not in st.session_state:
        st.session_state.api_token = ""

    token_input = st.text_input("Enter API Token", st.session_state.api_token)

    # Button to generate token
    if st.button("Generate Token"):
        try:
            response = requests.post(f"{FASTAPI_URL}/generate-token")
            token = response.json().get("token")
            st.session_state.api_token = token
            st.success(f"Token generated: {token}")
        except Exception as e:
            st.error(f"Error generating token: {e}")

    # --- Token Limit Section ---
    st.subheader("⚙️ Token Limit for LLM Response")

    token_limit = st.number_input(
        "Set maximum tokens for LLM response",
        min_value=10,
        max_value=2000,
        value=100,
        step=10
    )

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
                    json={"prompt": prompt, "token_limit": token_limit},
                    headers={"Authorization": f"Bearer {st.session_state.api_token}"}
                )

                if response.status_code == 200:
                    st.success("Response from LLM:")
                    st.write(response.json()["response"])
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Error calling backend: {e}")


# -----------------------------------------------------------
# ===========================================================
# TAB 2 - API SEARCH (New Section)
# ===========================================================
# -----------------------------------------------------------
with tab2:

    st.header("🔎 API Search")

    if "api_token" not in st.session_state:
        st.session_state.api_token = ""

    # Input prompt for search
    search_prompt = st.text_input("Enter search text")
    print(f"search_prompt {search_prompt}")
    if st.button("Search API"):
        if not st.session_state.api_token:
            st.error("Please generate or enter a token first.")
        else:
            try:
                # Example – call a different API endpoint
                response = requests.post(
                    f"{FASTAPI_URL}/ask_prompt",
                    json={"prompt": search_prompt},
                    headers={"Authorization": f"Bearer {st.session_state.api_token}"}
                )

                if response.status_code == 200:
                    st.success("Search Results:")
                    st.write(response.json()["response"])
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Error calling backend: {e}")
