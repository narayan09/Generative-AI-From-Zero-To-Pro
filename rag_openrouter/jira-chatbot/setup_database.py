# setup_database.py
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def run_sql_file(filepath):
    """Execute an SQL file against the MySQL server (without specifying database)."""
    cmd = f"mysql -h {DB_HOST} -P {DB_PORT} -u {DB_USER} -p{DB_PASSWORD} < {filepath}"
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def run_data_generation():
    print("Generating synthetic data...")
    subprocess.run(["python", "generate_jira_data.py"], check=True)

def export_dump():
    dump_file = "jira_tickets_dump.sql"
    cmd = f"mysqldump -h {DB_HOST} -P {DB_PORT} -u {DB_USER} -p{DB_PASSWORD} --databases {DB_NAME} > {dump_file}"
    print(f"Exporting database to {dump_file}...")
    subprocess.run(cmd, shell=True, check=True)
    print(f"Dump saved to {dump_file}")

if __name__ == "__main__":
    print("=== Setting up Jira Tickets Database ===")
    print("1. Applying schema...")
    run_sql_file("schema.sql")
    print("2. Generating data...")
    run_data_generation()
    print("3. Exporting SQL dump...")
    export_dump()
    print("=== Setup complete! ===")
    print(f"You can now import 'jira_tickets_dump.sql' into MySQL Workbench.")
    