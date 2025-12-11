Integrates CrewAI with Ollama

Uses ChatOllama (LangChain) for basic connectivity tests

Imports
import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from crewai import Agent, Task, Process, Crew, LLM


✔ os — Access environment variables
✔ ChatOllama — Direct LLM interface for Ollama (LangChain)
✔ HumanMessage — Message wrapper for LLM calls
✔ CrewAI components:

Agent – AI persona

Task – Work assigned to agent

Process – Execution style (sequential/parallel)

Crew – Orchestrates everything

LLM – Wrapper for LiteLLM model configs

Set dummy OpenAI key
os.environ["OPENAI_API_KEY"] = "sk-dummy-key-111"


✔ CrewAI internally expects an OpenAI key to exist,
even when using Ollama or OpenRouter.
✔ This dummy key prevents errors like:

ValueError: OPENAI_API_KEY not set

============================================================
1️⃣ Test Ollama Basic Connection
============================================================
def test_ollama():
    """Test basic Ollama connection with ChatOllama"""


✔ Function to verify if Ollama is running and model is loaded.

Create ChatOllama instance
llm = ChatOllama(model="phi3:mini", temperature=0.7)


✔ Uses local Ollama model
✔ No CrewAI here — pure LangChain test

Prepare prompt
prompt = HumanMessage(content="Hello Ollama! Tell me a fun fact about AI.")


✔ Human-style message created for LangChain.

Run LLM
response = llm.generate([[prompt]])


✔ generate expects list of conversations, so [ [prompt] ]
✔ Returns LangChain LLMResult

Print output
print(response.generations[0][0].text)


✔ Access nested generation:

generations[0] → first prompt response

[0] → first generation

.text → generated text

============================================================
2️⃣ CrewAI with Ollama (phi3:mini)
============================================================
def run_crew_with_phi3(task_description: str):


✔ A reusable CrewAI function where task is dynamic.

Create CrewAI LLM for Ollama
llm = LLM(
    model="ollama/phi3:mini",
    base_url="http://localhost:11434",
    api_key="dummy"
)


✔ CrewAI uses LiteLLM, so:

model="ollama/<model>" is MANDATORY

api_key is required (ignored for Ollama)

base_url must point to your Ollama server

Create an Agent
agent = Agent(
    role="General AI Agent",
    goal="Help with any task given by user",
    backstory="You are a helpful and intelligent assistant running on phi3:mini.",
    verbose=True,
    allow_delegation=True,
    llm=llm
)


✔ Defines an AI persona with:

a role

a goal

a backstory

connects it to the llm

detailed logs enabled

Create a Task
task = Task(
    description=task_description,
    expected_output="A clear, helpful answer.",
    agent=agent
)


✔ Task is dynamic (passed into the function)
✔ This task is assigned to the agent

Create Crew orchestrator
crew = Crew(
    agents=[agent],
    tasks=[task],
    model="ollama/phi3:mini",
    cache=True,
    verbose=True,
    process=Process.sequential,
    planning=True,
    planning_llm=llm
)


✔ CrewAI controller with:

Agents list

Tasks list

Default model

Sequential process (task executed step-by-step)

Planning enabled (CrewAI generates execution plan)

Planning LLM set

Run Crew
result = crew.kickoff()
return result


✔ Executes the entire pipeline
✔ Returns the final response

============================================================
3️⃣ CrewAI with OpenRouter
============================================================
def run_crew_with_openrouter(task_description: str):


✔ Same pattern as Ollama, but uses OpenRouter’s API.

Define OpenRouter LLM
llm = LLM(
    model="openrouter/meta-llama/llama-3.1-8b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


✔ Uses LiteLLM
✔ Requires REAL OpenRouter API key

Agent + Task + Crew

Same as the Ollama version but with OpenRouter model.

============================================================
Run tests
============================================================
if __name__ == "__main__":


✔ Script entry point.

✔ It runs:

response = run_crew_with_openrouter("Give me 5 unique business ideas in AI.")

✅ GITHUB-READY README.md

Below is a professional README.md for your repository.
You can copy-paste directly into GitHub.

📌 README.md
🚀 CrewAI + Ollama + OpenRouter Integration

A complete working example of CrewAI using:

🧠 Ollama (local LLMs)

🌍 OpenRouter (cloud LLMs)

🔗 LangChain ChatOllama connectivity test

This repository demonstrates how to:

✔ Test Ollama integration using ChatOllama
✔ Run CrewAI tasks using Ollama phi3:mini
✔ Run CrewAI tasks using OpenRouter models
✔ Use a reusable function pattern for different LLMs

📂 Project Structure
├── main.py            # Full CrewAI + Ollama + OpenRouter code
└── README.md          # Documentation

🚀 Features
1️⃣ Direct Ollama Connectivity Test

Uses ChatOllama (LangChain) to confirm your local model works.

2️⃣ CrewAI + Ollama

Runs an agentic task using a local model:

phi3:mini

ANY Ollama model is supported

Uses LiteLLM backend

3️⃣ CrewAI + OpenRouter

Run agent workflows using:

Llama 3.1 8B Instruct

GPT-4o-mini

Hermes 3

Qwen 2.5

Just change the model name.

🛠 Installation
pip install crewai litellm langchain_ollama langchain_core

⚙️ Environment Variables
OpenRouter (required for cloud models)
export OPENROUTER_API_KEY="your_api_key_here"

Dummy OpenAI key (required by CrewAI)

Already handled in code:

os.environ["OPENAI_API_KEY"] = "sk-dummy-key"

🔥 Running the Script
python main.py

🧪 Example Outputs
🔹 Ollama test
Hello! Fun fact: AI can learn complex tasks from simple patterns.

🔹 CrewAI (Ollama)
1. Automates workflows...
2. Helps break tasks into steps...

🔹 CrewAI (OpenRouter)
1. AI-based audit system...
2. Personalized learning engines...

✨ Customize Models
Ollama

In run_crew_with_phi3():

model="ollama/phi3:mini"


Change to:

ollama/llama3
ollama/qwen2.5
ollama/gemma2

OpenRouter
model="openrouter/meta-llama/llama-3.1-8b-instruct"


Replace with:

"openrouter/openai/gpt-4o-mini"

"openrouter/nousresearch/hermes-3-8b"

"openrouter/qwen/qwen2.5-7b-instruct"