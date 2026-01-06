import uuid

def generate_teams(cursor, workspace_id, num_teams=20):
    teams = []
    for i in range(num_teams):
        team_id = str(uuid.uuid4())
        name = f"Team {i+1}"
        teams.append((team_id, workspace_id, name))

    cursor.executemany(
        "INSERT INTO teams (team_id, workspace_id, name) VALUES (?, ?, ?)",
        teams
    )
    return [t[0] for t in teams]
