# 🎯 CrewAI - Practical Examples & Code Snippets for Tutors

## 📚 Table of Contents
1. Installation & Setup
2. Simple Examples (Beginner)
3. Intermediate Examples
4. Advanced Examples
5. Common Use Cases
6. Troubleshooting Guide

---

# 1️⃣ INSTALLATION & SETUP

## Step 1: Install CrewAI

```bash
# Using pip
pip install crewai crewai-tools

# Or using poetry
poetry add crewai crewai-tools
```

## Step 2: Get an API Key

### Option 1: OpenRouter (Recommended for Tutoring)
- Go to: https://openrouter.ai
- Sign up for free
- Create API key
- Cost: $0.0002-0.006 per 1K tokens (very cheap!)

### Option 2: OpenAI
- Go to: https://platform.openai.com
- Create API key
- Cost: $0.0005-0.06 per 1K tokens

### Option 3: Local Model (Free)
- Use Ollama: https://ollama.ai
- Download model: `ollama pull llama2`
- No API key needed!

## Step 3: Create .env File

```bash
# Create .env file in your project
cat > .env << EOF
OPENROUTER_API_KEY=your-api-key-here
OPENAI_API_KEY=your-openai-key-here
EOF
```

## Step 4: Import in Python

```python
from crewai import Agent, Task, Crew, LLM, Process
from crewai_tools import tool
```

---

# 2️⃣ SIMPLE EXAMPLES (BEGINNER)

## Example 1: Hello World - Single Agent

```python
from crewai import Agent, Task, Crew, LLM

# Step 1: Create LLM
llm = LLM(
    model="openrouter/meta-llama/llama-3.1-8b-instruct",
    api_key="your-openrouter-key"
)

# Step 2: Create Agent
greeting_agent = Agent(
    role="Friendly Assistant",
    goal="Greet people warmly",
    backstory="You are a friendly AI assistant",
    llm=llm,
    verbose=True
)

# Step 3: Create Task
greeting_task = Task(
    description="Say hello to John and ask how they're doing",
    agent=greeting_agent,
    expected_output="A friendly greeting message"
)

# Step 4: Create Crew
crew = Crew(
    agents=[greeting_agent],
    tasks=[greeting_task],
    verbose=True
)

# Step 5: Run it!
result = crew.kickoff()
print(result)
```

**Output might be:**
```
Hello John! 👋 
I hope you're having an amazing day! 
How are you doing? I'm here if you need anything!
```

## Example 2: Simple Math Problem

```python
from crewai import Agent, Task, Crew, LLM

llm = LLM(
    model="openrouter/meta-llama/llama-3.1-8b-instruct",
    api_key="your-key"
)

# Create a math tutor agent
math_tutor = Agent(
    role="Math Tutor",
    goal="Solve math problems step by step",
    backstory="Expert math teacher who explains clearly",
    llm=llm,
    verbose=True
)

# Create task
math_task = Task(
    description="""
    Solve this problem step by step:
    A train travels 150 km in 3 hours.
    What is its average speed?
    
    Show your work clearly.
    """,
    agent=math_tutor,
    expected_output="Step-by-step solution with final answer"
)

# Create crew and run
crew = Crew(agents=[math_tutor], tasks=[math_task])
result = crew.kickoff()
print(result)
```

## Example 3: Text Summarization

```python
from crewai import Agent, Task, Crew, LLM

llm = LLM(
    model="openrouter/meta-llama/llama-3.1-8b-instruct",
    api_key="your-key"
)

summarizer = Agent(
    role="Content Summarizer",
    goal="Summarize complex text into key points",
    backstory="Expert at finding main ideas",
    llm=llm
)

summarize_task = Task(
    description="""
    Summarize this text in 3 bullet points:
    
    "Artificial Intelligence is rapidly transforming industries
    across the world. From healthcare to finance, AI is enabling
    new possibilities and automating complex tasks. Machine learning,
    a subset of AI, allows systems to learn from data without
    explicit programming..."
    """,
    agent=summarizer,
    expected_output="3 key bullet points"
)

crew = Crew(agents=[summarizer], tasks=[summarize_task])
print(crew.kickoff())
```

**Output:**
```
• AI is transforming industries like healthcare and finance
• Machine learning enables systems to learn from data automatically
• AI is automating complex tasks and enabling new possibilities
```

---

# 3️⃣ INTERMEDIATE EXAMPLES

## Example 1: Multi-Agent Content Creation

```python
from crewai import Agent, Task, Crew, LLM, Process

llm = LLM(
    model="openrouter/meta-llama/llama-3.1-8b-instruct",
    api_key="your-key"
)

# Agent 1: Researcher
researcher = Agent(
    role="Research Specialist",
    goal="Find interesting facts and information",
    backstory="Thorough researcher who finds reliable sources",
    llm=llm,
    verbose=True
)

# Agent 2: Writer
writer = Agent(
    role="Content Writer",
    goal="Write engaging and clear content",
    backstory="Professional writer with 10+ years experience",
    llm=llm,
    verbose=True
)

# Agent 3: Editor
editor = Agent(
    role="Editor",
    goal="Improve content quality and clarity",
    backstory="Senior editor who polishes writing",
    llm=llm,
    verbose=True
)

# Task 1: Research
research_task = Task(
    description="Research 3 interesting facts about Python programming",
    agent=researcher,
    expected_output="List of 3 interesting Python facts with details"
)

# Task 2: Write
write_task = Task(
    description="Write a short paragraph about each fact from research",
    agent=writer,
    expected_output="3 paragraphs of content"
)

# Task 3: Edit
edit_task = Task(
    description="Review and improve the written content",
    agent=editor,
    expected_output="Final polished content"
)

# Create crew (tasks run in order)
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential,
    verbose=True
)

# Run
result = crew.kickoff()
print("=== FINAL RESULT ===")
print(result)
```

**How it works:**
1. Researcher finds facts
2. Writer uses researcher's facts to write
3. Editor polishes the writing
4. Final result is returned

## Example 2: Customer Support Team

```python
from crewai import Agent, Task, Crew, LLM, Process

llm = LLM(
    model="openrouter/meta-llama/llama-3.1-8b-instruct",
    api_key="your-key"
)

# Agent 1: Support Staff
support_staff = Agent(
    role="Customer Support Agent",
    goal="Help customers with basic issues",
    backstory="Friendly support agent with 5 years experience",
    llm=llm,
    verbose=True
)

# Agent 2: Manager
support_manager = Agent(
    role="Support Manager",
    goal="Handle complex issues and escalations",
    backstory="Manager with 15 years support experience",
    llm=llm,
    verbose=True
)

# Task 1: Initial support
support_task = Task(
    description="""
    A customer says: "I can't log into my account. 
    It keeps saying 'invalid password'"
    
    Try to help them first level support.
    """,
    agent=support_staff,
    expected_output="Solution or escalation note"
)

# Task 2: Manager review (if needed)
manager_task = Task(
    description="""
    Review the support agent's response.
    If the issue seems complex, provide 
    escalation guidance or better solution.
    """,
    agent=support_manager,
    expected_output="Final solution or escalation plan"
)

crew = Crew(
    agents=[support_staff, support_manager],
    tasks=[support_task, manager_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
print(result)
```

## Example 3: Code Review Team

```python
from crewai import Agent, Task, Crew, LLM

llm = LLM(
    model="openrouter/meta-llama/llama-3.1-8b-instruct",
    api_key="your-key"
)

# Agent 1: Security Expert
security_expert = Agent(
    role="Security Code Reviewer",
    goal="Find security vulnerabilities",
    backstory="Security expert with 10+ years experience",
    llm=llm
)

# Agent 2: Performance Expert
perf_expert = Agent(
    role="Performance Reviewer",
    goal="Identify performance issues",
    backstory="Performance optimization specialist",
    llm=llm
)

# Agent 3: Style Expert
style_expert = Agent(
    role="Code Style Reviewer",
    goal="Ensure code quality and readability",
    backstory="Senior developer with style expertise",
    llm=llm
)

# Sample code to review
sample_code = """
def user_login(username, password):
    db = connect_to_database()
    query = f"SELECT * FROM users WHERE name='{username}' AND pwd='{password}'"
    result = db.execute(query)
    if result:
        return True
    return False
"""

# Create tasks
security_task = Task(
    description=f"Review this code for security issues:\n{sample_code}",
    agent=security_expert,
    expected_output="List of security vulnerabilities"
)

perf_task = Task(
    description=f"Review this code for performance issues:\n{sample_code}",
    agent=perf_expert,
    expected_output="Performance improvements"
)

style_task = Task(
    description=f"Review this code for style issues:\n{sample_code}",
    agent=style_expert,
    expected_output="Style and readability improvements"
)

crew = Crew(
    agents=[security_expert, perf_expert, style_expert],
    tasks=[security_task, perf_task, style_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
```

---

# 4️⃣ ADVANCED EXAMPLES

## Example 1: Resume Screening (From Our Project)

```python
from crewai import Agent, Task, Crew, LLM, Process

llm = LLM(
    model="openrouter/meta-llama/llama-3.1-8b-instruct",
    api_key="your-key"
)

# Agent 1: Parser
parser = Agent(
    role="Resume Parser",
    goal="Extract resume information",
    backstory="HR expert with 10+ years experience",
    llm=llm,
    verbose=True
)

# Agent 2: Matcher
matcher = Agent(
    role="Skills Matcher",
    goal="Match candidate to job requirements",
    backstory="Recruiter with 15 years experience",
    llm=llm,
    verbose=True
)

# Agent 3: Assessor
assessor = Agent(
    role="Candidate Assessor",
    goal="Assess overall fit and potential",
    backstory="Senior hiring manager",
    llm=llm,
    verbose=True
)

# Tasks
parse_task = Task(
    description="""Extract from resume:
    1. Name, contact info
    2. Technical skills
    3. Work experience
    4. Education
    
    Resume:
    John Doe, john@example.com, (555)123-4567
    Senior Python Developer with 5 years experience
    Skills: Python, FastAPI, PostgreSQL, Docker
    Education: BS Computer Science
    """,
    agent=parser,
    expected_output="Structured resume data"
)

match_task = Task(
    description="""Match resume to requirements:
    Required: Python, React, Node.js, 5+ years
    
    Rate match from 0-100""",
    agent=matcher,
    expected_output="Match score 0-100 with explanation"
)

assess_task = Task(
    description="Give final recommendation: HIRE, INTERVIEW, or REJECT",
    agent=assessor,
    expected_output="Final recommendation with reasoning"
)

crew = Crew(
    agents=[parser, matcher, assessor],
    tasks=[parse_task, match_task, assess_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff()
```

## Example 2: Creating Custom Tools

```python
from crewai import Agent, Task, Crew, LLM
from crewai_tools import tool
import math

# Create custom tools
@tool("Calculate")
def calculate_math(operation: str) -> float:
    """
    Perform math calculations
    Input: "add 5 10", "multiply 3 4", "sqrt 16"
    Output: Result
    """
    try:
        parts = operation.split()
        op = parts[0].lower()
        
        if op == "sqrt":
            return math.sqrt(float(parts[1]))
        elif op == "add":
            return float(parts[1]) + float(parts[2])
        elif op == "multiply":
            return float(parts[1]) * float(parts[2])
        else:
            return "Unknown operation"
    except Exception as e:
        return f"Error: {str(e)}"

@tool("Convert")
def convert_units(conversion: str) -> str:
    """
    Convert between units
    Input: "5 km to miles", "100 pounds to kg"
    Output: Conversion result
    """
    # Parse input
    if "km to miles" in conversion:
        km = float(conversion.split()[0])
        miles = km * 0.621371
        return f"{km} km = {miles:.2f} miles"
    elif "pounds to kg" in conversion:
        lbs = float(conversion.split()[0])
        kg = lbs * 0.453592
        return f"{lbs} lbs = {kg:.2f} kg"
    return "Unsupported conversion"

# Create agent with tools
llm = LLM(
    model="openrouter/meta-llama/llama-3.1-8b-instruct",
    api_key="your-key"
)

calculator = Agent(
    role="Math Assistant",
    goal="Solve math problems using tools",
    backstory="Math tutor who uses tools",
    llm=llm,
    tools=[calculate_math, convert_units],
    verbose=True
)

task = Task(
    description="Calculate: sqrt(144), then convert 10 km to miles",
    agent=calculator,
    expected_output="Results of both calculations"
)

crew = Crew(agents=[calculator], tasks=[task])
result = crew.kickoff()
```

---

# 5️⃣ COMMON USE CASES

## Use Case 1: Blog Post Generation

```python
from crewai import Agent, Task, Crew, LLM, Process

def create_blog_crew(topic: str):
    llm = LLM(model="openrouter/meta-llama/llama-3.1-8b", api_key="key")
    
    researcher = Agent(
        role="Blog Researcher",
        goal=f"Research {topic} thoroughly",
        llm=llm
    )
    
    writer = Agent(
        role="Blog Writer",
        goal="Write engaging blog posts",
        llm=llm
    )
    
    editor = Agent(
        role="Blog Editor",
        goal="Polish and improve content",
        llm=llm
    )
    
    research_task = Task(
        description=f"Research {topic} and provide key points",
        agent=researcher,
        expected_output="Research outline"
    )
    
    write_task = Task(
        description=f"Write blog post about {topic}",
        agent=writer,
        expected_output="2000-word blog post"
    )
    
    edit_task = Task(
        description="Edit and polish blog post",
        agent=editor,
        expected_output="Final blog post"
    )
    
    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, write_task, edit_task],
        process=Process.sequential,
        verbose=True
    )
    
    return crew

# Use it
blog_crew = create_blog_crew("Python for Beginners")
result = blog_crew.kickoff()
print(result)
```

## Use Case 2: Email Automation

```python
from crewai import Agent, Task, Crew, LLM

def create_email_crew(client_name: str, issue: str):
    llm = LLM(model="openrouter/meta-llama/llama-3.1-8b", api_key="key")
    
    analyst = Agent(
        role="Issue Analyst",
        goal="Understand customer issues",
        llm=llm
    )
    
    writer = Agent(
        role="Email Writer",
        goal="Write professional responses",
        llm=llm
    )
    
    analyze_task = Task(
        description=f"Analyze issue: {issue}",
        agent=analyst,
        expected_output="Analysis of the issue"
    )
    
    write_task = Task(
        description=f"Write professional response email to {client_name}",
        agent=writer,
        expected_output="Professional email response"
    )
    
    crew = Crew(
        agents=[analyst, writer],
        tasks=[analyze_task, write_task],
        process=Process.sequential
    )
    
    return crew

# Use it
issue = "Customer complains product doesn't work as expected"
crew = create_email_crew("John Smith", issue)
print(crew.kickoff())
```

## Use Case 3: Data Analysis Report

```python
from crewai import Agent, Task, Crew, LLM

def create_analysis_crew(data_description: str):
    llm = LLM(model="openrouter/meta-llama/llama-3.1-8b", api_key="key")
    
    analyst = Agent(
        role="Data Analyst",
        goal="Analyze data and find patterns",
        llm=llm
    )
    
    visualizer = Agent(
        role="Report Writer",
        goal="Create clear reports",
        llm=llm
    )
    
    analysis_task = Task(
        description=f"Analyze: {data_description}",
        agent=analyst,
        expected_output="Key findings and statistics"
    )
    
    report_task = Task(
        description="Create professional report from analysis",
        agent=visualizer,
        expected_output="Complete analysis report"
    )
    
    crew = Crew(
        agents=[analyst, visualizer],
        tasks=[analysis_task, report_task],
        process=Process.sequential
    )
    
    return crew

# Use it
data = "Sales data for Q1 2024 showing revenue trends"
crew = create_analysis_crew(data)
print(crew.kickoff())
```

---

# 6️⃣ TROUBLESHOOTING GUIDE

## Problem 1: "API Key not found"

```python
# ❌ WRONG: Hardcoding key
llm = LLM(
    model="gpt-4",
    api_key="sk-..."  # Not secure!
)

# ✅ RIGHT: Use environment variable
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

llm = LLM(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY")
)
```

## Problem 2: "Agent not responding"

```python
# Possible causes and solutions:

# 1. Check if API key is valid
# 2. Check if model name is correct
# 3. Check internet connection
# 4. Try with verbose=True to see what's happening

agent = Agent(
    role="Helper",
    goal="Help with tasks",
    backstory="Assistant",
    llm=llm,
    verbose=True  # See what's happening
)

# 3. Try simpler task
task = Task(
    description="Say hello",  # Simple task first
    agent=agent,
    expected_output="A greeting"
)
```

## Problem 3: "Too slow / Expensive"

```python
# Solution: Use cheaper/faster model

# ❌ WRONG: Using expensive model
llm = LLM(model="gpt-4", api_key="...")  # $0.03/1K tokens

# ✅ RIGHT: Use Llama
llm = LLM(
    model="openrouter/meta-llama/llama-3.1-8b-instruct",
    api_key="..."  # $0.0002/1K tokens (150x cheaper!)
)
```

## Problem 4: "Results not as expected"

```python
# Solution: Improve task description

# ❌ VAGUE
task = Task(
    description="Analyze this",
    agent=agent
)

# ✅ CLEAR
task = Task(
    description="""
    Analyze this data and:
    1. Identify top 3 trends
    2. Explain each trend in 2-3 sentences
    3. Suggest one action for each trend
    
    Return as numbered list.
    """,
    agent=agent,
    expected_output="Numbered list of trends with explanations and actions"
)
```

## Problem 5: "Agent can't use tools"

```python
# Solution: Make sure tools are passed correctly

# ❌ WRONG
agent = Agent(
    role="Analyzer",
    goal="Analyze data",
    tools=[calculate]  # Tool object
)

# ✅ RIGHT
from crewai_tools import tool

@tool("Calculate")
def calculate(expr):
    return eval(expr)

agent = Agent(
    role="Analyzer",
    goal="Analyze data",
    tools=[calculate]  # Decorated function
)
```

## Problem 6: "Token limit exceeded"

```python
# Solution: Reduce task complexity or data size

# ❌ WRONG: Too much data
task = Task(
    description="Analyze 10,000 lines of data",
    agent=agent
)

# ✅ RIGHT: Chunk the data
for chunk in chunks:
    task = Task(
        description="Analyze this chunk of data",
        agent=agent
    )
    crew.kickoff(input={"data": chunk})
```

---

# 🎓 TEACHING TIPS

## For Students:

1. **Start with copy-paste**
   - Give them working examples
   - Let them run it
   - Then explain

2. **Show verbose output**
   - `verbose=True` shows thinking
   - Students see step-by-step
   - Easier to understand

3. **Use real problems**
   - Not just "hello world"
   - Resume screening, content generation
   - Something tangible

4. **Gradual complexity**
   - Start: 1 agent, 1 task
   - Then: 2-3 agents
   - Finally: 5+ agents with tools

5. **Let them experiment**
   - Change backstories
   - Change task descriptions
   - See how results change

## For Tutors:

1. **Have fallback examples**
   - If API key fails, use local model
   - Have cached results ready
   - Know how to explain errors

2. **Teach debugging**
   - `verbose=True`
   - Print intermediate results
   - Check API limits

3. **Show cost management**
   - Cheap vs expensive models
   - When to use which
   - Calculate project costs

4. **Connect to real jobs**
   - This is industry-standard
   - Companies use CrewAI
   - Valuable skill for careers

---

**Now you have practical examples for every situation!** 🚀

These can be directly copied and used in classroom or tutorials.
