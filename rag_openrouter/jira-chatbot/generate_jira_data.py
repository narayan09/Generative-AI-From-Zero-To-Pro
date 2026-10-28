# generate_jira_data.py
import os
import random
import mysql.connector
from faker import Faker
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

fake = Faker()

# Database connection
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

# --- Configuration ---
NUM_PROJECTS = 5
NUM_USERS = 30
NUM_ISSUES = 500
COMMENTS_PER_ISSUE_MIN = 1
COMMENTS_PER_ISSUE_MAX = 5

# --- 1. Insert Projects ---
project_keys = ["ALPHA", "BETA", "GAMMA", "DELTA", "EPS"]
for i, key in enumerate(project_keys, start=1):
    cursor.execute(
        "INSERT INTO projects (project_key, project_name, description) VALUES (%s, %s, %s)",
        (key, f"{key} Project", fake.catch_phrase())
    )
conn.commit()
print(f"Inserted {NUM_PROJECTS} projects.")

# --- 2. Insert Users ---
user_ids = []
for i in range(NUM_USERS):
    username = fake.user_name()
    display_name = fake.name()
    email = fake.email()
    cursor.execute(
        "INSERT INTO users (username, display_name, email) VALUES (%s, %s, %s)",
        (username, display_name, email)
    )
    user_ids.append(cursor.lastrowid)
conn.commit()
print(f"Inserted {NUM_USERS} users.")

# --- 3. Insert Issue Types ---
types = ["Bug", "Task", "Story", "Epic", "Sub-task"]
type_ids = {}
for t in types:
    cursor.execute("INSERT INTO issue_types (type_name) VALUES (%s)", (t,))
    type_ids[t] = cursor.lastrowid
conn.commit()

# --- 4. Insert Priorities ---
priorities = ["Blocker", "Critical", "Major", "Minor", "Trivial"]
priority_ids = {}
for p in priorities:
    cursor.execute("INSERT INTO priorities (priority_name) VALUES (%s)", (p,))
    priority_ids[p] = cursor.lastrowid
conn.commit()

# --- 5. Insert Statuses ---
statuses = ["Open", "In Progress", "Resolved", "Closed", "Reopened"]
status_ids = {}
for s in statuses:
    cursor.execute("INSERT INTO statuses (status_name) VALUES (%s)", (s,))
    status_ids[s] = cursor.lastrowid
conn.commit()

# --- 6. Insert Issues ---
issue_ids = []
issue_keys = []
start_date = datetime.now() - timedelta(days=180)  # issues from last 6 months

for i in range(NUM_ISSUES):
    project_id = random.randint(1, NUM_PROJECTS)
    project_key = project_keys[project_id - 1]
    issue_num = i + 1
    issue_key = f"{project_key}-{issue_num}"

    type_choice = random.choice(types)
    type_id = type_ids[type_choice]

    priority_choice = random.choices(priorities, weights=[5, 15, 40, 30, 10])[0]
    priority_id = priority_ids[priority_choice]

    status_choice = random.choice(statuses)
    status_id = status_ids[status_choice]

    assignee_id = random.choice(user_ids) if random.random() > 0.1 else None
    reporter_id = random.choice(user_ids)

    # Random date within the last 180 days
    created_date = fake.date_time_between(start_date=start_date, end_date="now")
    updated_date = created_date + timedelta(
        hours=random.randint(1, 48)
    )
    due_date = created_date + timedelta(days=random.randint(1, 30)) if random.random() > 0.3 else None

    summary = fake.sentence(nb_words=6)
    description = fake.paragraph(nb_sentences=3)
    resolution = fake.sentence() if status_choice in ("Resolved", "Closed") else None

    cursor.execute(
        """
        INSERT INTO issues 
        (issue_key, project_id, type_id, priority_id, status_id, summary, description, assignee_id, reporter_id, created_date, updated_date, due_date, resolution)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (issue_key, project_id, type_id, priority_id, status_id, summary, description, assignee_id, reporter_id, created_date, updated_date, due_date, resolution)
    )
    issue_ids.append(cursor.lastrowid)
    issue_keys.append(issue_key)

conn.commit()
print(f"Inserted {NUM_ISSUES} issues.")

# --- 7. Insert Comments ---
comment_count = 0
for issue_id in issue_ids:
    # Decide number of comments for this issue
    num_comments = random.randint(COMMENTS_PER_ISSUE_MIN, COMMENTS_PER_ISSUE_MAX)
    for _ in range(num_comments):
        author_id = random.choice(user_ids)
        comment_text = fake.paragraph(nb_sentences=2)
        # Comment created shortly after the issue or later
        cursor.execute("SELECT created_date FROM issues WHERE issue_id = %s", (issue_id,))
        issue_created = cursor.fetchone()[0]
        comment_date = fake.date_time_between(
            start_date=issue_created, end_date=issue_created + timedelta(days=30)
        )
        cursor.execute(
            "INSERT INTO comments (issue_id, author_id, comment_text, created_date) VALUES (%s, %s, %s, %s)",
            (issue_id, author_id, comment_text, comment_date)
        )
        comment_count += 1

conn.commit()
print(f"Inserted {comment_count} comments.")

# Cleanup
cursor.close()
conn.close()
print("Data generation complete.")