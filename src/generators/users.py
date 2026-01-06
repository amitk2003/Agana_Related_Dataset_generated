import uuid
from faker import Faker
import random

fake = Faker()

def generate_users(cursor, team_ids, num_users=6000):
    users = []
    for _ in range(num_users):
        user_id = str(uuid.uuid4())
        name = fake.name()
        email = fake.unique.email()
        team_id = random.choice(team_ids)

        users.append((user_id, name, email, team_id))

    cursor.executemany(
        "INSERT INTO users (user_id, name, email, team_id) VALUES (?, ?, ?, ?)",
        users
    )
    return [u[0] for u in users]
