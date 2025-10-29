from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


# Initialize Ollama model (no API key needed!)
llm = ChatOllama(
    model="phi3:mini",
    temperature=0.7,
)

# Create a simple chain
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
chain = prompt | llm | StrOutputParser()

# 1 Use it to call chain
result = chain.invoke({"topic": "Python programming"})
print(result)
#2

# Step 1: Initialize your Ollama model
llm = ChatOllama(model="phi3:mini")  # or "mistral", "phi3", etc.

# Step 2: Create message objects
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hello, how are you?"),
    AIMessage(content="I'm doing well, thank you!"),
    HumanMessage(content="Can you explain LangChain in simple terms?")
]

# Step 3: Send the conversation to the model
response = llm.invoke(messages)

# Step 4: Display the result
print(response.content)

