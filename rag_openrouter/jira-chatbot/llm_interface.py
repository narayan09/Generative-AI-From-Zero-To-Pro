# llm_interface.py
import os
import re
import ollama
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMInterface:
    def __init__(self):
        self.ollama_enabled = os.getenv("OLLAMA_ENABLED", "true").lower() == "true"
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o")

        if self.openrouter_api_key:
            self.openrouter_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_api_key,
            )
        else:
            self.openrouter_client = None

    def _extract_sql(self, text: str) -> str:
        """Extract a SQL query from the LLM response, stripping markdown."""
        # Remove common code fences
        text = re.sub(r'```sql\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'```\s*', '', text)
        return text.strip()

    def generate_sql(self, question: str, schema_text: str) -> str:
        """
        Convert a natural language question to a SQL query.
        Raises an exception if all attempts fail.
        """
        system_prompt = f"{schema_text}\n\nRules:\n- Output ONLY the raw SQL query.\n- Do not include any explanation."

        # Try Ollama first
        if self.ollama_enabled:
            try:
                client = ollama.Client(host=self.ollama_host)
                response = client.chat(
                    model=self.ollama_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    options={"temperature": 0.1}
                )
                raw = response['message']['content']
                sql = self._extract_sql(raw)
                if sql.upper().startswith("SELECT"):
                    return sql
                else:
                    # If not a SELECT, maybe the model added an explanation; try again with a stricter prompt?
                    raise ValueError(f"Model returned non-SELECT: {sql[:100]}")
            except Exception as e:
                print(f"[Ollama] Error: {e}. Falling back to OpenRouter.")

        # Fallback to OpenRouter
        if self.openrouter_client:
            try:
                completion = self.openrouter_client.chat.completions.create(
                    model=self.openrouter_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.1,
                    max_tokens=500
                )
                raw = completion.choices[0].message.content
                sql = self._extract_sql(raw)
                if sql.upper().startswith("SELECT"):
                    return sql
                else:
                    raise ValueError(f"OpenRouter returned non-SELECT: {sql[:100]}")
            except Exception as e:
                raise RuntimeError(f"Both LLM providers failed. Last error: {e}")
        else:
            raise RuntimeError("Ollama is disabled or unavailable, and no OpenRouter API key is configured.")
        
    def chat(self, system_prompt: str, user_message: str) -> str:
        """General chat completion (for RAG). Uses the same fallback strategy."""
        if self.ollama_enabled:
            try:
                client = ollama.Client(host=self.ollama_host)
                response = client.chat(
                    model=self.ollama_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    options={"temperature": 0.3}
                )
                return response['message']['content']
            except Exception as e:
                print(f"[Ollama chat] Error: {e}. Trying OpenRouter...")

        if self.openrouter_client:
            try:
                completion = self.openrouter_client.chat.completions.create(
                    model=self.openrouter_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.3,
                )
                return completion.choices[0].message.content
            except Exception as e:
                raise RuntimeError(f"Both providers failed: {e}")
        else:
            raise RuntimeError("No LLM provider available.")