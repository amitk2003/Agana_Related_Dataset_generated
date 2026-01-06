import sqlite3
import os
from generators.team_memberships import generate_team_memberships
from generators.sections import generate_sections
# from generators.sections import section_map
from generators.teams import generate_teams
from generators.users import generate_users
from generators.projects import generate_projects
from generators.tasks import generate_tasks
from generators.tags import generate_tags, generate_task_tags
from generators.comments import generate_comments
from generators.custom_fields import (
    generate_custom_fields,
    generate_custom_field_values
)



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "output", "asana_Totaldataset.sqlite")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


def setup_database():
    os.makedirs("output", exist_ok=True)
    # delete old data if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    return conn, cursor

def main():
    conn, cursor = setup_database()

    workspace_id = "workspace-001"
    cursor.execute(
        "INSERT INTO workspaces (workspace_id, name) VALUES (?, ?)",
        (workspace_id, "Demo SaaS Company")
    )

    team_ids = generate_teams(cursor, workspace_id)
    user_ids = generate_users(cursor,team_ids)
    generate_team_memberships(cursor, team_ids, user_ids)

    projects = generate_projects(cursor, workspace_id, team_ids)
    section_map = generate_sections(cursor, projects)
    generate_tasks(cursor, projects, section_map, user_ids)
    cursor.execute("SELECT task_id, project_id FROM tasks")
    tasks = [
    {"task_id": r[0], "project_id": r[1]}
    for r in cursor.fetchall()
] 
    task_ids = [t["task_id"] for t in tasks]
    tag_ids = generate_tags(cursor)
    generate_task_tags(cursor, task_ids, tag_ids)

    generate_comments(cursor, task_ids, user_ids)

    field_defs = generate_custom_fields(cursor, projects)
    generate_custom_field_values(cursor, tasks, field_defs)



    conn.commit()
    conn.close()
    print("✅ Asana seed database generated successfully")

if __name__ == "__main__":
    main()


# “I explicitly reset the database on each generation run to avoid contamination across experiments, which is critical when generating evaluation datasets for RL environments.”