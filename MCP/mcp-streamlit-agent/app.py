import streamlit as st
import subprocess, json, requests
from common.jsonrpc import request
import re
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def extract_json(text):
    """
    Extract JSON object from LLM response text
    """
    # Remove markdown code fences if present
    text = text.strip()

    # Case 1: ```json ... ```
    if text.startswith("```"):
        text = re.sub(r"^```json", "", text)
        text = re.sub(r"^```", "", text)
        text = re.sub(r"```$", "", text)
        text = text.strip()

    # Extract first JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM response")

    return json.loads(match.group())


def call_mcp(method, query):
    proc = subprocess.Popen(
        ["python", "mcp_server/tools_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    payload = request(method, {"query": query})
    out, _ = proc.communicate(payload)
    return json.loads(out)["result"]


def ask_llm(prompt):
    res = requests.post(OLLAMA_URL, json={
        "model": "phi3:mini",
        "prompt": prompt,
        "stream": False
    })
    return res.json()["response"]

def get_tools():
    proc = subprocess.Popen(
        ["python", "mcp_server/tools_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    out, _ = proc.communicate(request("tools.list", {}, 99))
    return json.loads(out)["result"]


def decide_tool(user_query, tools):
    system_prompt = f"""
You are an AI agent.
Choose exactly ONE tool.

Available tools:
{json.dumps(tools, indent=2)}

Rules:
- Respond ONLY with JSON
- No explanation
- No markdown

JSON format:
{{
  "tool": "<tool name>",
  "arguments": {{
    "query": "<string>"
  }}
}}
"""

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": system_prompt + "\nUser query: " + user_query,
            "stream": False
        }
    )

    raw_text = res.json()["response"]
    print("🔎 Raw LLM output:\n", raw_text)

    return extract_json(raw_text)

st.title("🧠 MCP Streamlit Agent")

query = st.text_input("Ask something:")

if st.button("Ask"):
    tools = get_tools()

    decision = decide_tool(query, tools)

    tool_name = decision["tool"]
    args = decision["arguments"]

    st.info(f"🔧 Tool selected by LLM: `{tool_name}`")

    result_data = call_mcp(tool_name, args["query"])

    st.success("✅ Tool executed")
    st.write(result_data)
