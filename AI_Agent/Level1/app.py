"""
Level 1 AI Agent — Streamlit Chat UI
Standalone LLM chatbot with Groq streaming.

Run with:
    streamlit run app.py
"""

import streamlit as st
from agent import stream_response, MODELS, DEFAULT_SYSTEM_PROMPT, count_tokens_estimate

# ─── Page config ────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Level 1 AI Agent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Chat message styling */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 8px;
    }

    /* Input area */
    .stChatInputContainer {
        border-top: 1px solid #e0e0e0;
        padding-top: 12px;
    }

    /* Sidebar */
    .sidebar-section {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
    }

    /* Stats badge */
    .stat-badge {
        background: #e8f4fd;
        color: #1565c0;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: 500;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── Session state init ──────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_tokens_est" not in st.session_state:
    st.session_state.total_tokens_est = 0

if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# ─── Sidebar ────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("⚙️ Settings")

    st.subheader("Model")
    selected_model_name = st.selectbox(
        "Choose Groq model",
        options=list(MODELS.keys()),
        index=0,
        help="LLaMA 3.3 70B gives the best quality. LLaMA 3.1 8B is the fastest.",
    )
    selected_model = MODELS[selected_model_name]

    st.caption(f"Model ID: `{selected_model}`")

    st.divider()

    st.subheader("Parameters")

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Higher = more creative. Lower = more focused and deterministic.",
    )

    max_tokens = st.slider(
        "Max response tokens",
        min_value=256,
        max_value=4096,
        value=1024,
        step=256,
        help="Maximum length of each response.",
    )

    st.divider()

    st.subheader("System prompt")
    system_prompt = st.text_area(
        "Customize the assistant's persona",
        value=DEFAULT_SYSTEM_PROMPT,
        height=140,
        help="This is the hidden instruction that shapes how the model behaves.",
    )

    st.divider()

    st.subheader("Session stats")
    col1, col2 = st.columns(2)
    col1.metric("Messages", st.session_state.message_count)
    col2.metric("~Tokens used", st.session_state.total_tokens_est)

    if st.button("🗑️ Clear chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.total_tokens_est = 0
        st.session_state.message_count = 0
        st.rerun()

    st.divider()
    st.caption("**Level 1 Agent** · Standalone LLM · Groq + Streamlit")
    st.caption("No tools · No memory · No planning")

# ─── Main chat area ──────────────────────────────────────────────────────────

st.title("🤖 Level 1 AI Agent")
st.caption("Standalone LLM · Powered by Groq · Streaming enabled")

# Show welcome message if no chat yet
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "👋 Hello! .\n\n"
            "I'm a standalone LLM — no tools, no memory between sessions, "
            "just fast, streamed responses. Ask me anything!\n\n"
            "**Try these:**\n"
            "- `Explain how neural networks work in simple terms`\n"
            "- `Write a Python function to reverse a linked list`\n"
            "- `What's the difference between REST and GraphQL?`"
        )

# Render existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─── Chat input & streaming response ────────────────────────────────────────

if user_input := st.chat_input("Ask me anything..."):

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.message_count += 1
    st.session_state.total_tokens_est += count_tokens_estimate(user_input)

    # Build messages for API (last 20 turns to stay within context)
    history = st.session_state.messages[-20:]

    # Stream the response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            for chunk in stream_response(
                messages=history,
                model=selected_model,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=system_prompt,
            ):
                full_response += chunk
                # Show response as it streams in, with blinking cursor
                response_placeholder.markdown(full_response + "▌")

            # Final render without cursor
            response_placeholder.markdown(full_response)

        except ValueError as e:
            # API key missing
            st.error(f"⚠️ Configuration error: {e}")
            st.info(
                "**To fix this:**\n"
                "1. Get a free API key at [console.groq.com](https://console.groq.com)\n"
                "2. Copy `.env.example` to `.env`\n"
                "3. Add your key: `GROQ_API_KEY=gsk_...`\n"
                "4. Restart the app"
            )
            full_response = f"Error: {e}"

        except Exception as e:
            st.error(f"⚠️ Groq API error: {e}")
            full_response = f"Error: {e}"

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.message_count += 1
    st.session_state.total_tokens_est += count_tokens_estimate(full_response)