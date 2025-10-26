from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize Ollama model (no API key needed!)
llm = ChatOllama(
    model="phi3:mini",
    temperature=0.7,
)

# Create a simple chain
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
chain = prompt | llm | StrOutputParser()

# Use it
result = chain.invoke({"topic": "Python programming"})
print(result)
