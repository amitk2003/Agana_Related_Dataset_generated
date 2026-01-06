import uuid

SECTION_TEMPLATES = {
    "engineering": ["Backlog", "In Progress", "Code Review", "Done"],
    "marketing": ["Ideation", "Creation", "Review", "Published"],
    "operations": ["To Do", "In Progress", "Waiting", "Done"]
}

def generate_sections(cursor, projects):
    section_map = {}

    for project in projects:
        project_id = project["project_id"]
        project_type = project["type"]

        section_map[project_id] = []

        for pos, name in enumerate(SECTION_TEMPLATES[project_type]):
            section_id = str(uuid.uuid4())

            cursor.execute(
                """
                INSERT INTO sections (section_id, project_id, name, position)
                VALUES (?, ?, ?, ?)
                """,
                (section_id, project_id, name, pos)
            )

            section_map[project_id].append(section_id)

    return section_map
