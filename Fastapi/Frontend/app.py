import streamlit as st
import requests

st.set_page_config(page_title="AI Chat with Ollama", layout="centered")

st.title("💬 Chat with Ollama (phi3:mini)")
st.caption("FastAPI + Streamlit + Ollama")

# Chat history in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input
user_input = st.text_area("🗨️ Your message:", placeholder="Ask anything...")

# When button clicked
if st.button("Send"):
    if not user_input.strip():
        st.warning("Please enter a message first.")
    else:
        with st.spinner("Ollama thinking..."):
            try:
                res = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"message": user_input},
                    timeout=120
                )
                if res.status_code == 200:
                    reply = res.json().get("response", "")
                    st.session_state.messages.append(("🧑 You", user_input))
                    st.session_state.messages.append(("🤖 Ollama", reply))
                else:
                    st.error(f"Backend error {res.status_code}")
            except Exception as e:
                st.error(f"❌ Connection error: {e}")

# Display chat
st.divider()
for role, msg in st.session_state.messages:
    if role == "🧑 You":
        st.markdown(f"**{role}:** {msg}")
    else:
        st.markdown(f"<div style='background-color:#eef;padding:10px;border-radius:10px;'>"
                    f"**{role}:** {msg}</div>", unsafe_allow_html=True)
