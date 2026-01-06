import random

def generate_team_memberships(cursor, team_ids, user_ids):
    memberships = []

    for user_id in user_ids:
        teams = random.sample(team_ids, k=random.randint(1, 2))
        for team_id in teams:
            memberships.append((team_id, user_id))

    cursor.executemany(
        """
        INSERT INTO team_memberships (team_id, user_id)
        VALUES (?, ?)
        """,
        memberships
    )
