"""
Level 1 AI Agent — LangChain + Groq Integration
Core inference logic with streaming support, now powered by LangChain.
"""

import os
from typing import Iterator, List, Dict, Optional

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessageChunk, HumanMessage, SystemMessage, BaseMessage
from langchain_groq import ChatGroq

load_dotenv()

# Available Groq models (same as before)
MODELS = {
    "LLaMA 3.3 70B (best quality)": "llama-3.3-70b-versatile",
    "LLaMA 3.1 8B (fastest)": "llama-3.1-8b-instant",
    "Mixtral 8x7B (balanced)": "mixtral-8x7b-32768",
    "Gemma 2 9B (efficient)": "gemma2-9b-it",
}

DEFAULT_SYSTEM_PROMPT = """You are a helpful, knowledgeable, and concise AI assistant powered by Groq.
You respond clearly and directly. When writing code, always include language identifiers in code blocks.
Keep responses focused and avoid unnecessary padding."""

# ----------------------------------------------------------------------
# Cached LLM factory (Streamlit)
# ----------------------------------------------------------------------
@st.cache_resource
def get_llm(
    model_name: str,
    temperature: float,
    max_tokens: int,
) -> ChatGroq:
    """
    Returns a cached ChatGroq instance.
    Caching is keyed by model, temperature, and max_tokens.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Please set it in your .env file or environment variables."
        )
    return ChatGroq(
        model=model_name,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        streaming=True,   # enables .stream() even when using .invoke()
    )


# ----------------------------------------------------------------------
# Message conversion
# ----------------------------------------------------------------------
def _convert_to_langchain_messages(
    messages: List[Dict[str, str]],
    system_prompt: Optional[str] = None,
) -> List[BaseMessage]:
    """
    Convert a list of dict messages (with 'role' and 'content') into
    a list of LangChain BaseMessage objects. Prepends a system message
    if a system prompt is provided.
    """
    lc_messages = []
    if system_prompt:
        lc_messages.append(SystemMessage(content=system_prompt))
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            lc_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            lc_messages.append(AIMessageChunk(content=content))
        else:
            # Unexpected role – treat as human for safety
            lc_messages.append(HumanMessage(content=content))
    return lc_messages


# ----------------------------------------------------------------------
# Streaming response (yields text chunks)
# ----------------------------------------------------------------------
def stream_response(
    messages: List[Dict[str, str]],
    model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
) -> Iterator[str]:
    """
    Stream a response from Groq LLM using LangChain.

    Args:
        messages: List of {"role": "user"/"assistant", "content": "..."} dicts
        model: Groq model identifier (e.g., "llama-3.3-70b-versatile")
        temperature: 0.0 (deterministic) to 1.0 (creative)
        max_tokens: Maximum tokens in response
        system_prompt: System instruction for the model

    Yields:
        str: Text chunks as they stream in
    """
    llm = get_llm(model, temperature, max_tokens)
    lc_messages = _convert_to_langchain_messages(messages, system_prompt)

    for chunk in llm.stream(lc_messages):
        # chunk is an AIMessageChunk; its content is a string
        if chunk.content:
            yield chunk.content


# ----------------------------------------------------------------------
# Non‑streaming full response
# ----------------------------------------------------------------------
def get_full_response(
    messages: List[Dict[str, str]],
    model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.7,
    max_tokens: int = 2048,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
) -> str:
    """
    Get a complete (non‑streaming) response from Groq.
    Useful for testing or non‑UI contexts.
    """
    llm = get_llm(model, temperature, max_tokens)
    lc_messages = _convert_to_langchain_messages(messages, system_prompt)
    response = llm.invoke(lc_messages)
    return response.content


# ----------------------------------------------------------------------
# Token estimation (unchanged)
# ----------------------------------------------------------------------
def count_tokens_estimate(text: str) -> int:
    """Rough token estimate: ~4 chars per token."""
    return len(text) // 4