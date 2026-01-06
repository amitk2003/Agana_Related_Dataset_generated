import uuid
import random
from utils.vocab import (
    ENGINEERING_PROJECTS,
    MARKETING_PROJECTS,
    OPS_PROJECTS
)

PROJECT_TYPES = ["engineering", "marketing", "operations"]

def generate_projects(cursor, workspace_id, team_ids, num_projects=30):
    projects = []
    project_meta = []

    for _ in range(num_projects):
        project_id = str(uuid.uuid4())
        project_type = random.choice(PROJECT_TYPES)

        if project_type == "engineering":
            name = random.choice(ENGINEERING_PROJECTS)
        elif project_type == "marketing":
            name = random.choice(MARKETING_PROJECTS)
        else:
            name = random.choice(OPS_PROJECTS)

        description = f"{name} planned for the current quarter."
        team_id = random.choice(team_ids)

        projects.append(
            (project_id, workspace_id, team_id, name, description)
        )

        project_meta.append({
            "project_id": project_id,
            "type": project_type,
            "team_id": team_id
        })

    cursor.executemany(
        """
        INSERT INTO projects (project_id, workspace_id, team_id, name, description)
        VALUES (?, ?, ?, ?, ?)
        """,
        projects
    )

    return project_meta
