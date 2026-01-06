import uuid
import random
from datetime import timedelta

COMMENTS_POOL = [
    "Please review this when you get time.",
    "Blocked due to dependency, will update.",
    "This looks good to me.",
    "Let’s discuss this in standup.",
    "Can we prioritize this?",
    "Pushing this to next sprint.",
    "Needs clarification from stakeholders."
]

def generate_comments(cursor, task_ids, user_ids):
    comments = []

    for task_id in task_ids:
        if random.random() < 0.4:  # 40% tasks have comments
            for _ in range(random.randint(1, 3)):
                comment_id = str(uuid.uuid4())
                user_id = random.choice(user_ids)
                text = random.choice(COMMENTS_POOL)

                comments.append(
                    (comment_id, task_id, user_id, text)
                )

    cursor.executemany(
        """
        INSERT INTO comments (comment_id, task_id, user_id, text)
        VALUES (?, ?, ?, ?)
        """,
        comments
    )
