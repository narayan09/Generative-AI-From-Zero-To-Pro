# CrewAI with Ollama & OpenRouter

A working example of CrewAI using local Ollama models via `langchain_ollama` and hosted OpenRouter models. This project demonstrates both approaches with minimal, clean code that's easy to extend.

## Features

- **Local AI**: Run CrewAI with Ollama models (`phi3:mini`) directly on your machine
- **Hosted AI**: Switch to OpenRouter's models (`llama-3.1-8b-instruct`) with one line change
- **Planning Enabled**: Uses CrewAI's built-in planner for better task execution
- **Beginner-Friendly**: Clear structure with separate functions for each approach
- **Production-Ready**: Proper error handling patterns and environment variable management

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running (for local model)
- Ollama model: `phi3:mini` (pull with `ollama pull phi3:mini`)
- OpenRouter API key (for hosted model option)

## Installation


## Environment Setup

### Required Variables

The script automatically sets a dummy OpenAI key (required by CrewAI internally):
os.environ["OPENAI_API_KEY"] = "sk-dummy-key-111"

### OpenRouter API Key (Optional)

For the hosted model example, set your API key:
export OPENROUTER_API_KEY="your-key-here" # Linux/macOS

or
set OPENROUTER_API_KEY=your-key-here # Windows Command Prompt


## Usage

The script includes three test functions. Uncomment the ones you want to run in the `__main__` block.

### 1. Test Basic Ollama Connection

In main block:
test_ollama()

text

Verifies that Ollama is running and `phi3:mini` responds correctly.

### 2. Run CrewAI with Local Ollama

In main block:
response = run_crew_with_phi3("Your task description here")
print(response)

text

Creates a CrewAI agent powered by your local `phi3:mini` model.

### 3. Run CrewAI with OpenRouter

In main block:
response = run_crew_with_openrouter("Your task description here")
print(response)

text

Creates a CrewAI agent using OpenRouter's hosted model.

### Current Default

The script is currently configured to run the OpenRouter example:

response = run_crew_with_openrouter("Give me 5 unique business ideas in AI.")

text

## Code Structure

### `test_ollama()`
- Direct LangChain Ollama test
- Uses `ChatOllama` and `HumanMessage`
- Simple sanity check for local setup

### `run_crew_with_phi3(task_description)`
- CrewAI agent with local Ollama
- `LLM(model="ollama/phi3:mini")`
- Single agent, single task, sequential process
- Planning enabled with `planning_llm`

### `run_crew_with_openrouter(task_description)`
- Same structure, but uses OpenRouter
- `LLM(model="openrouter/meta-llama/llama-3.1-8b-instruct")`
- Requires valid `OPENROUTER_API_KEY`

## Customization

### Change Local Model
In run_crew_with_phi3()
llm = LLM(model="ollama/llama3", base_url="http://localhost:11434", api_key="dummy")

text

### Change Hosted Model
In run_crew_with_openrouter()
llm = LLM(model="openrouter/anthropic/claude-3.5-sonnet", base_url="https://openrouter.ai/api/v1", api_key=...)

text

### Add More Agents
researcher = Agent(role="Researcher", goal="Gather information", backstory="...", llm=llm)
writer = Agent(role="Writer", goal="Create content", backstory="...", llm=llm)
crew = Crew(agents=[researcher, writer], tasks=[task1, task2], process=Process.sequential)

text

## Important Notes

- **Never commit API keys**: The dummy OpenAI key is safe, but keep your OpenRouter key in environment variables only
- **Ollama must be running**: Start it with `ollama serve` before running local tests
- **Model names matter**: Use the exact format `ollama/model-name` for local and `openrouter/provider/model` for hosted
- **CrewAI version**: This code works with CrewAI's current LLM abstraction. Check for API changes if you upgrade

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `OPENAI_API_KEY not found` | Ensure the dummy key is set at the top of the script |
| Ollama connection error | Check `ollama serve` is running and `phi3:mini` is pulled |
| OpenRouter auth error | Verify `OPENROUTER_API_KEY` environment variable is set correctly |
| Model not found | Check model name spelling and availability on Ollama/OpenRouter |

## License

MIT License - feel free to use this in your projects!

---

**Happy building with CrewAI!** For questions or issues, please open an issue in this repository.
Would you like me to also create a requirements.txt file with specific version pins for the dependencies?







