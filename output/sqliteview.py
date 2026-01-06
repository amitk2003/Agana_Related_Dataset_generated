import sqlite3
from pprint import pprint

DB_PATH = "asana_simulation.sqlite"  # adjust path if needed

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n--- TABLES ---")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
pprint(tables)

print("\n--- ROW COUNTS ---")
for (table,) in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table}: {count}")

print("\n--- SAMPLE TASKS ---")
cursor.execute("""
    SELECT task_id, name, due_date, completed
    FROM tasks
    LIMIT 5
""")
pprint(cursor.fetchall())

print("\n--- ASSIGNEE INTEGRITY CHECK ---")
cursor.execute("""
    SELECT COUNT(*)
    FROM tasks t
    LEFT JOIN users u ON t.assignee_id = u.user_id
    WHERE t.assignee_id IS NOT NULL
      AND u.user_id IS NULL
""")
print("Broken assignee references:", cursor.fetchone()[0])

conn.close()
