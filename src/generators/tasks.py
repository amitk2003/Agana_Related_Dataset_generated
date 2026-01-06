import uuid
import random
from datetime import timedelta
from utils.vocab import (
    ENGINEERING_TASKS, ENGINEERING_COMPONENTS,
    MARKETING_TASKS, MARKETING_ASSETS
)
# from .sections import section_map
from utils.dates import random_future_date, random_past_datetime

def generate_task_name(project_type):
    if project_type == "engineering":
        return f"{random.choice(ENGINEERING_TASKS)} {random.choice(ENGINEERING_COMPONENTS)}"
    elif project_type == "marketing":
        return f"{random.choice(MARKETING_TASKS)} {random.choice(MARKETING_ASSETS)}"
    else:
        return "Review operational workflow"

def generate_task_description(task_name):
    return f"""
Objective:
{task_name}

Details:
- Review current implementation
- Apply necessary changes
- Validate with stakeholders

Acceptance Criteria:
- No regressions introduced
- Task meets expected outcome
""".strip()

def generate_tasks(cursor, projects,section_map, user_ids, tasks_per_project=200):
    tasks = []

    for project in projects:
        project_id = project["project_id"]
        project_type = project["type"]
        section_id = random.choice(section_map[project_id])

        parent_tasks = []

        for _ in range(tasks_per_project):
            task_id = str(uuid.uuid4())
            name = generate_task_name(project_type)
            description = generate_task_description(name)

            assignee = (
                random.choice(user_ids)
                if random.random() > 0.15 else None
            )

            created_at = random_past_datetime(days_back=180)
            completed = random.random() < 0.65

            completed_at = (
                created_at + timedelta(days=random.randint(1, 14))
                if completed else None
            )

            due_date = random_future_date(max_days=90)

            parent_task_id = (
                random.choice(parent_tasks)
                if parent_tasks and random.random() < 0.25
                else None
            )

            tasks.append((
                task_id,
                project_id,
                section_id,
                parent_task_id,
                name,
                description,
                assignee,
                due_date,
                created_at,
                completed,
                completed_at
            ))

            if parent_task_id is None:
                parent_tasks.append(task_id)

    cursor.executemany(
        """
        INSERT INTO tasks (
            task_id, project_id, section_id, parent_task_id,
            name, description, assignee_id, due_date,
            created_at, completed, completed_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        tasks
    )
