# Advanced Prompt Techniques Guide: Complete Learning Resource

## Introduction
This guide covers 10+ essential prompt engineering techniques with practical examples using OpenRouter API. Each technique is demonstrated with code examples and practice questions.

---

## 1. Zero-Shot Prompting
**Definition**: Asking the model to perform a task without any examples or prior context.

### Code Example
```python
import requests

API_KEY = "sk-or-v1-b3286fe9600bd3ff3b58d7a392e6f59e32221cc"
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Zero-Shot: No examples provided
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": "Classify the following text as positive or negative sentiment: 'The product quality is amazing and exceeded my expectations!'"
        }
    ],
    "max_tokens": 100
}

response = requests.post(url, headers=headers, json=data)
print("Zero-Shot Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- Simple, straightforward tasks
- When the task is self-explanatory
- For common knowledge questions

---

## 2. Few-Shot Prompting
**Definition**: Providing a few examples to guide the model's behavior.

### Code Example
```python
# Few-Shot: Examples provided
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": """Classify the sentiment of product reviews:

Example 1: "This is amazing! Love it!" → Positive
Example 2: "Terrible quality, waste of money" → Negative
Example 3: "It's okay, nothing special" → Neutral

Now classify this: "Great value for money, would buy again!"
Answer: """
        }
    ],
    "max_tokens": 50
}

response = requests.post(url, headers=headers, json=data)
print("Few-Shot Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- When you want consistent output format
- For nuanced classification tasks
- When zero-shot doesn't provide desired results

---

## 3. Chain-of-Thought (CoT) Prompting
**Definition**: Asking the model to explain its reasoning step-by-step.

### Code Example
```python
# Chain-of-Thought: Request step-by-step reasoning
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": """Solve this step-by-step:
            
If a store has 50 apples and sells 30% of them, then receives 20 more apples, how many apples does it have?

Please think through this step-by-step, showing each calculation."""
        }
    ],
    "max_tokens": 200
}

response = requests.post(url, headers=headers, json=data)
print("CoT Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- Complex reasoning tasks
- Mathematical problem-solving
- Multi-step logic problems

---

## 4. Role-Playing / System Prompt Technique
**Definition**: Instructing the model to adopt a specific persona or role.

### Code Example
```python
# Role-Playing: System role definition
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "You are an expert Python software architect with 15 years of experience. Provide concise, production-ready code examples."
        },
        {
            "role": "user",
            "content": "Explain what is a design pattern and give me a practical example."
        }
    ],
    "max_tokens": 300
}

response = requests.post(url, headers=headers, json=data)
print("Role-Playing Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- Need specific expertise level
- Want consistent personality/tone
- Educational content generation

---

## 5. Instruction-Based Prompting
**Definition**: Providing explicit, detailed instructions for the task.

### Code Example
```python
# Instruction-Based: Detailed step-by-step instructions
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": """Generate a Python function with these requirements:
1. Function name: calculate_bmi
2. Takes two parameters: weight (kg) and height (m)
3. Returns BMI as a float rounded to 2 decimal places
4. Include docstring with example usage
5. Add type hints for all parameters and return value

Format: Provide only the function code, no explanation."""
        }
    ],
    "max_tokens": 200
}

response = requests.post(url, headers=headers, json=data)
print("Instruction-Based Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- When you need specific output format
- Technical code generation
- Complex requirements specification

---

## 6. Comparative Prompting
**Definition**: Asking the model to compare and contrast different options.

### Code Example
```python
# Comparative: Asking for comparison
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": """Compare REST APIs and GraphQL in the context of a real-time collaborative document editor.

Structure your response as:
1. REST APIs - Advantages & Disadvantages
2. GraphQL - Advantages & Disadvantages
3. Which is better for this use case and why?"""
        }
    ],
    "max_tokens": 400
}

response = requests.post(url, headers=headers, json=data)
print("Comparative Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- Decision-making scenarios
- Technology evaluation
- Trade-off analysis

---

## 7. Summarization Prompting
**Definition**: Asking the model to condense information to key points.

### Code Example
```python
# Summarization: Asking for specific summary format
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": """Summarize the following text in 3 bullet points:

Machine learning is a subset of artificial intelligence that focuses on the development 
of algorithms that can learn from data. Instead of being explicitly programmed, these 
algorithms improve their performance through experience. Common types include supervised 
learning, unsupervised learning, and reinforcement learning. Applications range from 
recommendation systems to autonomous vehicles.

Bullet points should be concise and capture the main ideas."""
        }
    ],
    "max_tokens": 150
}

response = requests.post(url, headers=headers, json=data)
print("Summarization Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- Information compression
- Content distillation
- Key takeaway extraction

---

## 8. Question Answering (QA) Prompting
**Definition**: Providing context and asking specific questions about it.

### Code Example
```python
# QA Prompting: Context + specific questions
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": """Context: 
CrewAI is a framework for orchestrating role-playing autonomous agents. 
It enables you to build multi-agent systems where each agent has specific roles, 
goals, and tools. Agents can collaborate to accomplish complex tasks.

Questions:
1. What is the primary purpose of CrewAI?
2. Name three components that define an agent in CrewAI.
3. How do agents interact in a CrewAI system?

Answer each question concisely."""
        }
    ],
    "max_tokens": 250
}

response = requests.post(url, headers=headers, json=data)
print("QA Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- Educational content
- Knowledge extraction
- Information retrieval tasks

---

## 9. Creativity/Generation Prompting
**Definition**: Asking the model to generate creative content with guidance.

### Code Example
```python
# Creativity: Creative generation with constraints
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": """Generate a creative story with these constraints:
1. Genre: Science Fiction
2. Length: 2-3 sentences
3. Main character: A lonely AI learning to feel emotions
4. Setting: A space station
5. Ending: Hopeful but bittersweet"""
        }
    ],
    "max_tokens": 200
}

response = requests.post(url, headers=headers, json=data)
print("Creativity Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- Content creation
- Brainstorming
- Imaginative problem-solving

---

## 10. Debugging/Error Analysis Prompting
**Definition**: Asking the model to identify and fix issues in code or logic.

### Code Example
```python
# Debugging: Code analysis and fix
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": """Find and fix the bugs in this Python function:

def calculate_average(numbers):
    total = 0
    for num in numbers
        total = total + num
    average = total / len(numbers)
    return average

Provide:
1. List of bugs found
2. Corrected code
3. Brief explanation of each fix"""
        }
    ],
    "max_tokens": 250
}

response = requests.post(url, headers=headers, json=data)
print("Debugging Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- Code review and improvement
- Learning from mistakes
- Quality assurance

---

## 11. Structured Output Prompting
**Definition**: Requesting output in a specific structured format (JSON, markdown, etc.).

### Code Example
```python
# Structured Output: JSON format requested
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": """Provide information about Python in JSON format:

{
    "language": "Python",
    "use_case_1": {
        "name": "",
        "description": ""
    },
    "use_case_2": {
        "name": "",
        "description": ""
    },
    "pros": [],
    "cons": []
}

Fill in all fields with appropriate information."""
        }
    ],
    "max_tokens": 300
}

response = requests.post(url, headers=headers, json=data)
print("Structured Output Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- API integration
- Data parsing requirements
- Structured data generation

---

## 12. Adversarial Prompting / Red Teaming
**Definition**: Challenging the model to find weaknesses or alternative perspectives.

### Code Example
```python
# Adversarial: Asking for counterarguments
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": """Statement: "Microservices architecture is always better than monolithic architecture."

Provide strong counterarguments to this statement:
1. List 3 scenarios where monolithic is better
2. Explain the hidden costs of microservices
3. Give a real-world example where monolithic succeeded"""
        }
    ],
    "max_tokens": 350
}

response = requests.post(url, headers=headers, json=data)
print("Adversarial Response:", response.json()["choices"][0]["message"]["content"])
```

### When to Use
- Critical thinking development
- Balanced analysis
- Identifying blind spots

---

## Complete Practice Script

```python
import requests
import json

API_KEY = "sk-or-v1-b3286fe9600bd3ff3b58d7a392e6f59e32221cc"
url = "https://openrouter.ai/api/v1/chat/completions"

def make_request(prompt, technique_name):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        print(f"\n{'='*60}")
        print(f"Technique: {technique_name}")
        print(f"{'='*60}")
        print(result["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"Error with {technique_name}: {e}")

# Test all techniques
prompts = {
    "Zero-Shot": "What are the benefits of machine learning?",
    "Few-Shot": "Classify sentiment - Good product→Positive, Bad product→Negative. New: Great quality→?",
    "Chain-of-Thought": "If you have 100 apples, give 25 to friend A, 30 to friend B, keep rest. How many left? Think step-by-step.",
    "Role-Playing": "You are a cybersecurity expert. Explain what a phishing attack is.",
    "Instruction-Based": "Create a Python function that reverses a string. Use type hints and include docstring.",
    "Comparative": "Compare Python vs JavaScript for web development.",
    "Summarization": "Summarize this in 2 sentences: AI is revolutionizing technology. Deep learning powers many applications.",
    "QA": "Context: Python is a programming language. Q: Is Python suitable for data science?",
    "Creativity": "Write a 2-sentence creative story about a robot discovering friendship.",
    "Debugging": "Fix this: def add(a,b) return a+b. Provide corrected code.",
    "Structured Output": "Provide Python pros in JSON: {\"pros\": [...]}",
    "Adversarial": "Counter the statement: 'AI will replace all human programmers.'"
}

for technique, prompt in prompts.items():
    make_request(prompt, technique)
```

---

## Practice Questions for Self-Assessment

### Beginner Level
1. **Zero-Shot vs Few-Shot**: When would you use each approach? Give an example where few-shot would be better than zero-shot.

2. **Chain-of-Thought Application**: Write a prompt using CoT for the problem: "A store has 200 items. 40% are sold, then 50 more are added. How many remain?"

3. **Role Definition**: Define a system role for a prompt where you want the model to act as a "Data Science Educator."

### Intermediate Level
4. **Multi-Technique Prompt**: Create a single prompt that combines:
   - Few-shot examples
   - Chain-of-thought reasoning
   - Structured output format

5. **Comparative Analysis**: Using comparative prompting, ask the model to compare two AI frameworks (e.g., CrewAI vs AutoGen). What structure would you use?

6. **Error Detection**: Identify which prompting technique would be best for:
   - Teaching a student mathematics
   - Generating creative blog titles
   - Fixing code bugs
   - Extracting key information from text

### Advanced Level
7. **Prompt Optimization**: You have a basic prompt: "Explain machine learning." Create three variations using different techniques and predict which would produce the best result. Why?

8. **Constraint-Based Generation**: Write a prompt that asks the model to:
   - Generate a security-focused Python function
   - Include specific security considerations
   - Provide both the code and explanation
   - Use structured output format

9. **Iterative Refinement**: Design a multi-turn conversation (system message + multiple user messages) that guides the model to build a complete project plan for a CrewAI application.

10. **Adversarial Thinking**: Create an adversarial prompt that tests whether the model can:
    - Identify limitations of a technology you're promoting
    - Suggest better alternatives in specific scenarios
    - Explain trade-offs honestly

### Expert Challenge
11. **Prompt Engineering Workflow**: Design a complete workflow combining 3+ techniques to:
    - Analyze a real problem statement
    - Generate multiple solution approaches
    - Compare solutions
    - Provide structured implementation guidance

12. **Meta-Learning**: Create a prompt that teaches the model about effective prompt engineering, then use that in a follow-up prompt. Document the impact on response quality.

---

## Key Takeaways

| Technique | Best For | Difficulty |
|-----------|----------|-----------|
| Zero-Shot | Simple tasks | Easy |
| Few-Shot | Pattern learning | Easy |
| Chain-of-Thought | Complex reasoning | Medium |
| Role-Playing | Expertise simulation | Easy |
| Instruction-Based | Specific formats | Medium |
| Comparative | Decision-making | Medium |
| Summarization | Compression | Easy |
| QA | Knowledge extraction | Easy |
| Creativity | Generation | Hard |
| Debugging | Problem-solving | Medium |
| Structured Output | Data integration | Medium |
| Adversarial | Critical thinking | Hard |

---

## Next Steps for Practice

1. **Run the Complete Practice Script**: Execute the script provided above with your API key
2. **Answer Self-Assessment Questions**: Work through all 12 practice questions
3. **Create Custom Prompts**: Design your own prompts for your specific use cases
4. **Combine Techniques**: Experiment mixing 2-3 techniques in a single prompt
5. **Measure Results**: Track which techniques work best for your specific domain
6. **Iterate**: Refine prompts based on output quality and relevance

---

## Resources for Further Learning

- Study how responses differ between techniques
- Document what works best for your use cases
- Create a prompt library for your projects
- Practice adversarial prompting to identify model limitations
- Experiment with temperature and max_tokens parameters to see impact