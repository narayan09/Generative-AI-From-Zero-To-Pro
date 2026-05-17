import time
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Content Writer",
    page_icon="✍️",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 20px;
}

.stTextArea textarea {
    font-size: 16px;
}

.output-box {
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 10px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("✍️ AI Content Writer")
st.caption("Powered by Ollama + Qwen2.5 + LangChain + Streamlit")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("⚙️ Settings")

model_name = st.sidebar.selectbox(
    "Select Model",
    [
        "qwen2.5:3b",
        "phi3:mini",
        "llama3.1:8b"
    ]
)

content_type = st.sidebar.selectbox(
    "Content Type",
    [
        "Blog Post",
        "LinkedIn Post",
        "Instagram Caption",
        "SEO Article",
        "Email",
        "YouTube Script",
        "Product Description"
    ]
)

tone = st.sidebar.selectbox(
    "Tone",
    [
        "Professional",
        "Friendly",
        "Casual",
        "Technical",
        "Marketing",
        "Persuasive"
    ]
)

temperature = st.sidebar.slider(
    "Creativity",
    0.0,
    1.0,
    0.7,
    0.1
)

max_tokens = st.sidebar.slider(
    "Max Tokens",
    100,
    3000,
    800,
    100
)

# ---------------------------------------------------
# MAIN INPUT
# ---------------------------------------------------

prompt_input = st.text_area(
    "📝 Enter your prompt",
    height=220,
    placeholder="Example: Write a LinkedIn post about AI agents helping businesses automate repetitive work"
)

extra_input = st.text_input(
    "Additional Instructions",
    placeholder="SEO optimized, add CTA, use simple English, etc."
)

# ---------------------------------------------------
# BUTTON
# ---------------------------------------------------

generate = st.button(
    "🚀 Generate Content",
    use_container_width=True
)

# ---------------------------------------------------
# GENERATE CONTENT
# ---------------------------------------------------

if generate:

    if not prompt_input.strip():
        st.warning("Please enter a prompt.")
        st.stop()

    try:

        # Start Timer
        start_time = time.time()

        with st.spinner("Generating content..."):

            # Initialize Model
            llm = ChatOllama(
                model=model_name,
                temperature=temperature,
                num_predict=max_tokens,
            )

            # Prompt Template
            template = """
            You are an expert AI content writer.

            Write a high-quality {content_type}.

            Tone:
            {tone}

            User Request:
            {prompt_input}

            Additional Instructions:
            {extra_input}

            Requirements:
            - Make content engaging
            - Use proper formatting
            - Avoid repetitive wording
            - Keep it human-like
            """

            prompt = ChatPromptTemplate.from_template(template)

            chain = prompt | llm

            response = chain.invoke({
                "content_type": content_type,
                "tone": tone,
                "prompt_input": prompt_input,
                "extra_input": extra_input
            })

            # End Timer
            end_time = time.time()

            response_time = round(end_time - start_time, 2)

            output = response.content

            # ---------------------------------------------------
            # OUTPUT
            # ---------------------------------------------------

            st.success("✅ Content Generated Successfully")

            st.info(f"⏱️ Response Time: {response_time} seconds")

            st.subheader("📄 Generated Content")

            st.markdown(
                f"""
                <div class="output-box">
                {output}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader("📋 Copy Content")

            st.text_area(
                "Generated Output",
                value=output,
                height=300
            )

            st.download_button(
                label="⬇️ Download Content",
                data=output,
                file_name="generated_content.txt",
                mime="text/plain"
            )

    except Exception as e:

        st.error("❌ Error occurred")

        st.code(str(e))

        st.info("""
Make sure:

1. Ollama is installed
2. Ollama server is running
3. Model is downloaded

Run:

ollama serve
        """)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption("Local AI App using Ollama + LangChain + Streamlit")