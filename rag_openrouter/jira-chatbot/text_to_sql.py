# text_to_sql.py
import os
from db_connector import JiraDatabase
from llm_interface import LLMInterface

class TextToSQL:
    def __init__(self):
        self.db = JiraDatabase()
        self.llm = LLMInterface()
        # Load the static system prompt from file (contains schema + instructions)
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "system_sql.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def ask(self, question: str) -> dict:
        """
        Returns a dict with:
        - 'question': original question
        - 'sql': generated SQL query (str)
        - 'data': pandas DataFrame of results
        - 'error': None or error message string
        """
        result = {
            "question": question,
            "sql": None,
            "data": None,
            "error": None
        }
        try:
            # Step 1: LLM generates SQL
            sql = self.llm.generate_sql(question, self.system_prompt)
            result["sql"] = sql

            # Step 2: Validate and execute
            if not sql.lower().startswith("select"):
                raise ValueError("Generated query is not a SELECT statement.")

            # Step 3: Execute
            df = self.db.execute_query(sql)
            result["data"] = df

        except Exception as e:
            result["error"] = str(e)
            # Optionally: retry logic could be added here

        return result