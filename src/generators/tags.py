import uuid
import random

DEFAULT_TAGS = [
    "backend", "frontend", "urgent", "blocked",
    "high-priority", "low-priority",
    "bug", "feature", "marketing", "ops"
]

def generate_tags(cursor):
    tag_ids = {}

    for tag in DEFAULT_TAGS:
        tag_id = str(uuid.uuid4())
        tag_ids[tag] = tag_id
        cursor.execute(
            "INSERT INTO tags (tag_id, name) VALUES (?, ?)",
            (tag_id, tag)
        )

    return tag_ids


def generate_task_tags(cursor, task_ids, tag_ids):
    mappings = []

    for task_id in task_ids:
        if random.random() < 0.5:  # 50% tasks have tags
            chosen = random.sample(
                list(tag_ids.values()),
                k=random.randint(1, 2)
            )
            for tag_id in chosen:
                mappings.append((task_id, tag_id))

    cursor.executemany(
        "INSERT INTO task_tags (task_id, tag_id) VALUES (?, ?)",
        mappings
    )
