-- Organizations/Workspaces (top-level)
CREATE TABLE workspaces (
    workspace_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    team_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Teams
CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    workspace_id TEXT,
    name TEXT NOT NULL,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id)
);

-- Team memberships (many-to-many)
CREATE TABLE team_memberships (
    team_id TEXT,
    user_id TEXT,
    PRIMARY KEY (team_id, user_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Projects
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    workspace_id TEXT,
    team_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

-- Sections
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT,
    name TEXT NOT NULL,  -- e.g., "To Do"
    position INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Tasks (includes subtasks)
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT,
    section_id TEXT,
    parent_task_id TEXT,  -- NULL for top-level
    name TEXT NOT NULL,
    description TEXT,
    assignee_id TEXT,
    due_date DATE,
    created_at TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id)
);

-- Comments
CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT,
    user_id TEXT,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tags
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE task_tags (
    task_id TEXT,
    tag_id TEXT,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

-- Custom Fields (flexible)
CREATE TABLE custom_field_definitions (
    field_id TEXT PRIMARY KEY,
    project_id TEXT,
    name TEXT NOT NULL,  -- e.g., "Priority"
    type TEXT NOT NULL   -- e.g., "select", "number"
);

CREATE TABLE custom_field_values (
    value_id TEXT PRIMARY KEY,
    task_id TEXT,
    field_id TEXT,
    value TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id)
);
