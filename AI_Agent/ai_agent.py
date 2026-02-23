import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from typing import TypedDict
from langgraph.graph import StateGraph, END
#pip install -U langchain langgraph langchain-groq langchain-tavily

# Load environment variables
load_dotenv()

# Initialize LLM
groq_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=100
)

# Initialize Tavily tool (NEW package)
search_tool = TavilySearch(max_results=2,include_images=False )  # force boolean)

# Create agent (NEW API)
agent = create_agent(
    model=groq_llm,
    tools=[search_tool],
    system_prompt="You are a smart and friendly AI chatbot."
)

# Invoke agent
# response = agent.invoke(
#     {"messages": [{"role": "user", "content": "Tell me about trends in crypto"}]}
# )

# print(response["messages"][-1].content)

#Start → LLM → Tool → LLM → Final Answer
#Create a graph that takes input and sends it to LLM.

class GraphState(TypedDict):
    message:str
    response:str


def chatbot_node(state:GraphState):
    print(f"State Received:", state)
    result = groq_llm.invoke(state["message"])
    return {"response":result.content}

def example1(message):

    builder = StateGraph(GraphState)
    builder.add_node("chatbot",chatbot_node)
    builder.set_entry_point("chatbot")
    builder.add_edge("chatbot",END)
    graph = builder.compile()

    # 5️⃣ Execute
    result = graph.invoke({"message": message})

    return result

# ex1 =example1("Explain smart contracts")
# print(f"Response {ex1}")

#Conditional Routing (Agent behavior)
#         ┌── Tool Node
# User → Router
#         └── LLM Node
# 1️⃣ Define state
# 2️⃣ Define LLM
# 3️⃣ Define node functions
# 4️⃣ Define router
# 5️⃣ Build graph
# 6️⃣ Compile
# 7️⃣ Invoke
def llm_node(state: GraphState):
    result = groq_llm.invoke(state["message"])
    return {"response": result.content}

#weather Node
def weather_node(state:GraphState):
    return  {"response": "Weather is sunny today!"}

def calculator_node(state: GraphState):
    try:
        answer = eval(state["message"])
        return {"response": f"Answer is {answer}"}
    except:
        return {"response": "Invalid math expression"}
    
#Router Function (Agent Brain)
def router(state:GraphState):
    message= state["message"].lower()
    if "weather" in message:
        return "weather_node"
    
    if any(char.isdigit() for char in message):
        return "calculator_node"
    
    return "llm_node"


def example2(message):
    builder = StateGraph(GraphState)
    builder.add_node("llm_node",llm_node)
    builder.add_node("weather_node",weather_node)
    builder.add_node("calculator_node",calculator_node)

    # Conditional entry point
    builder.set_conditional_entry_point(router)

    builder.add_edge("llm_node", END)
    builder.add_edge("weather_node", END)
    builder.add_edge("calculator_node", END)

    graph = builder.compile()
    result = graph.invoke({"message": message})
    return result

# ex2=example2("25 * 4")
# ex2=example2("What is the weather?")
# print(ex2)

#LLM-powered router

# This is how production agents decide which tool to use.

# We are going to build:

# 🧠 LLM-Powered Intelligent Router in LangGraph

# No rule-based if/else.
# The LLM decides the route.
# 🧠 Architecture Logic

# Step 1 → Router Node calls LLM
# Step 2 → LLM returns structured decision
# Step 3 → Graph routes accordingly
class GraphStateLLM(TypedDict):
    message: str
    route: str
    response: str

def llm_router(state: GraphStateLLM):
    prompt = f"""
    You are an intent classifier.

    Classify the user message into one of these categories:
    - weather
    - calculator
    - general

    Only return one word.

    Message: {state["message"]}
    """

    result = groq_llm.invoke(prompt)
    decision = result.content.strip().lower()

    return {"route": decision}

def weather_node_llm(state: GraphStateLLM):
    return {"response": "Weather is sunny ☀️"}

def calculator_node_llm(state: GraphStateLLM):
    try:
        answer = eval(state["message"])
        return {"response": f"Answer is {answer}"}
    except:
        return {"response": "Invalid math expression"}
    
def general_llm_node(state: GraphStateLLM):
    result = groq_llm.invoke(state["message"])
    return {"response": result.content}

def route_decision(state: GraphStateLLM):
    return state["route"]

def example3(message):
    

    builder = StateGraph(GraphStateLLM)

    builder.add_node("router", llm_router)
    builder.add_node("weather", weather_node_llm)
    builder.add_node("calculator", calculator_node_llm)
    builder.add_node("general", general_llm_node)

    builder.set_entry_point("router")

    builder.add_conditional_edges(
        "router",
        route_decision,
        {
            "weather": "weather",
            "calculator": "calculator",
            "general": "general"
        }
    )

    builder.add_edge("weather", END)
    builder.add_edge("calculator", END)
    builder.add_edge("general", END)

    graph = builder.compile()
    return graph.invoke({"message": message})

print(example3("Will it rain today?"))