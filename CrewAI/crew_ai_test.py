"""
CrewAI with Ollama - Working version using langchain_ollama
Uses ChatOllama for direct Ollama integration
"""

import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from crewai import Agent, Task, Process, Crew, LLM

# Set dummy OPENAI_API_KEY at module level (required by CrewAI internally)
os.environ["OPENAI_API_KEY"] = "sk-dummy-key-111"


# ============================================================
# 1️⃣ Test Ollama Basic Connection
# ============================================================
def test_ollama():
    """Test basic Ollama connection with ChatOllama"""
    llm = ChatOllama(model="phi3:mini", temperature=0.7)

    prompt = HumanMessage(content="Hello Ollama! Tell me a fun fact about AI.")

    # Note: double brackets for generate
    response = llm.generate([[prompt]])

    print("=== Ollama Response ===")
    print(response.generations[0][0].text)


# ============================================================
# 2️⃣ CrewAI with ChatOllama (RECOMMENDED - Works with CrewAI)
# ============================================================
def run_crew_with_phi3(task_description: str):
    # Create LLM object
    llm = LLM(
        model="ollama/phi3:mini",
        base_url="http://localhost:11434",
        api_key="dummy"       # Required for LiteLLM, ignored by Ollama
    )

    

    # Create agent
    agent = Agent(
        role="General AI Agent",
        goal="Help with any task given by user",
        backstory="You are a helpful and intelligent assistant running on phi3:mini.",
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    # Create task
    task = Task(
        description=task_description,
        expected_output="A clear, helpful answer.",
        agent=agent
    )

    # Create crew
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

    # Run the crew
    result = crew.kickoff()
    return result



# ============================================================
# 3 CrewAI with openrouter (RECOMMENDED - Works with CrewAI)
# ============================================================
def run_crew_with_openrouter(task_description: str):
    llm = LLM(
        model="openrouter/meta-llama/llama-3.1-8b-instruct", 
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    agent = Agent(
        role="General AI Agent",
        goal="Help with any task using OpenRouter models",
        backstory="You are a knowledgeable agent running on an OpenRouter model.",
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    task = Task(
        description=task_description,
        expected_output="A helpful, correct, structured answer.",
        agent=agent
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        model="openrouter/meta-llama/llama-3.1-8b-instruct",
        verbose=True,
        cache=True,
        process=Process.sequential,
        planning=True,
        planning_llm=llm
    )

    return crew.kickoff()

# ============================================================
# Run Tests
# ============================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("TEST 1: Basic Ollama Connection")
    print("="*60 + "\n")
    # try:
    #     test_ollama()
    # except Exception as e:
    #     print(f"❌ Error: {e}")

    # print("\n" + "="*60)
    

    # response = run_crew_with_phi3("Write 5 benefits of learning Agentic AI.")
    # print("\nFinal Output:\n", response)

    response = run_crew_with_openrouter("Give me 5 unique business ideas in AI.")
    print("\nFinal Output:\n", response)

    #print(os.getenv("OPENROUTER_API_KEY"))
