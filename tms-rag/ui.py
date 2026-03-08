import streamlit as st
import requests

API_URL = "http://localhost:8000/query"  # Change if deployed elsewhere

st.set_page_config(page_title="TMS Shipment Assistant", page_icon="🚚")
st.title("🚚 TMS Shipment Assistant")
st.markdown("Ask me anything about shipments, parcels, tracking, etc.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type your question..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send to API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": prompt})
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # Optional: show sources in expander
                    with st.expander("See sources"):
                        for i, src in enumerate(data["sources"]):
                            st.write(f"**Source {i+1}:** {src}")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to API: {e}")