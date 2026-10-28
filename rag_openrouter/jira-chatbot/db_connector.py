# db_connector.py
import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class JiraDatabase:
    def __init__(self):
        db_config = {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", 3306)),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
        }
        self.pool = pooling.MySQLConnectionPool(
            pool_name="jira_pool",
            pool_size=3,
            **db_config
        )

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute a SELECT query and return results as a DataFrame."""
        conn = self.pool.get_connection()
        try:
            return pd.read_sql(query, conn)
        finally:
            conn.close()

    def get_schema_text(self) -> str:
        """Return a concise string representation of the schema for the prompt."""
        # We already have a detailed schema in the prompt file, but we could dynamically generate it.
        # For simplicity, we'll read the static prompt file.
        # However, if the schema changes, we'd want to auto-generate.
        # Here we'll keep it dynamic for robustness.
        schema_lines = ["Tables and columns:"]
        tables = ["projects", "users", "issue_types", "priorities", "statuses", "issues", "comments"]
        for table in tables:
            df = self.execute_query(f"DESCRIBE `{table}`")
            cols = []
            for _, row in df.iterrows():
                cols.append(f"{row['Field']} ({row['Type']})")
            schema_lines.append(f"- {table}: {', '.join(cols)}")
        return "\n".join(schema_lines)

    def get_sample_data(self, table: str, limit: int = 3) -> pd.DataFrame:
        """Return a few rows from a table for prompt examples."""
        return self.execute_query(f"SELECT * FROM `{table}` LIMIT {limit}")