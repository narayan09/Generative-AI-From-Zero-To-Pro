""" Goal: Understand multi-agent philosophy and build first crew
Key Concepts:
CrewAI vs. LangChain vs. AutoGen vs. LangGraph
Agent anatomy (role, goal, backstory)
Task anatomy (description, expected_output)
Crew execution flow
Exercises:
1A: Build your first crew
1B: Backstory experiment
1C: Debugging challenge
1D: Industry-specific agent """

###Example 1 
# Step 1: Install CrewAI
# Step 2: Import
# Step 3: Create the Agent
# Step 4: Create a Task for the Agent
# Step 5: Create the Crew and Run
# Step 6: Execute
from crewai import Agent, Task, Crew, LLM  # type: ignore

# Step 3: Create the Agent with Groq LLM
researcher = Agent(
    role="Senior Research Analyst",
    goal="Find and summarize 3 credible sources on any given topic",
    backstory=(
        "You have 10 years of experience in research journalism. "
        "You are meticulous about fact-checking and always cite your sources. "
        "You write clear, concise summaries that non-experts can understand."
    ),
    llm=LLM(model="groq/llama-3.3-70b-versatile"),  # <-- ADD THIS
    verbose=True
)

# Step 4: Create a Task for the Agent
research_task = Task(
    description="Research the topic: 'AI agent frameworks in 2026'. "
                "Find 3 key frameworks, their main features, and why they matter.",
    expected_output="A bullet-point summary with 3 frameworks, each with: name, key feature, and one-sentence why it matters.",
    agent=researcher
)

# Step 5: Create the Crew and Run
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True
)

# Step 6: Execute
result = crew.kickoff()
print("\n=== FINAL RESULT ===")
print(result)