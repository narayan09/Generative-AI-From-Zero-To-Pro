# pip install langchain langchain_ollama crewai

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import crewai
# -------------------------------
# 1️⃣ Test Ollama
# -------------------------------
def test_ollama():
    llm = ChatOllama(model="phi3:mini", temperature=0.7)

    prompt = HumanMessage(content="Hello Ollama! Tell me a fun fact about AI.")

    # Note: double brackets for generate
    response = llm.generate([[prompt]])

    print("=== Ollama Response ===")
    print(response.generations[0][0].text)


# -------------------------------
# 2️⃣ Test CrewAI
# -------------------------------
def test_crewai():
    # Check available attributes
    print("Available CrewAI attributes:", dir(crewai))

    from crewai import Agent

    print("CrewAI version:", crewai.__version__)

   

# -------------------------------
# 3️⃣ Run Both Tests
# -------------------------------
if __name__ == "__main__":
    #test_ollama()
    test_crewai()
