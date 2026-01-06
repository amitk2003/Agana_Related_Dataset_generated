import uuid
import random

FIELD_TEMPLATES = [
    ("Priority", "select", ["Low", "Medium", "High"]),
    ("Effort", "number", ["1", "2", "3", "5", "8"]),
]

def generate_custom_fields(cursor, projects):
    field_defs = []

    for project in projects:
        for name, field_type, _ in FIELD_TEMPLATES:
            field_id = str(uuid.uuid4())
            field_defs.append(
                (field_id, project["project_id"], name, field_type)
            )

    cursor.executemany(
        """
        INSERT INTO custom_field_definitions
        (field_id, project_id, name, type)
        VALUES (?, ?, ?, ?)
        """,
        field_defs
    )

    return field_defs
def generate_custom_field_values(cursor, tasks, field_defs):
    values = []

    for task in tasks:
        task_id = task["task_id"]
        project_id = task["project_id"]

        for field_id, proj_id, name, field_type in field_defs:
            if proj_id != project_id:
                continue

            if random.random() < 0.8:  # 80% tasks have fields
                value = (
                    random.choice(["Low", "Medium", "High"])
                    if name == "Priority"
                    else random.choice(["1", "2", "3", "5", "8"])
                )

                values.append(
                    (str(uuid.uuid4()), task_id, field_id, value)
                )

    cursor.executemany(
        """
        INSERT INTO custom_field_values
        (value_id, task_id, field_id, value)
        VALUES (?, ?, ?, ?)
        """,
        values
    )

