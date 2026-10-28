-- schema.sql
CREATE DATABASE IF NOT EXISTS jira_tickets_db;
USE jira_tickets_db;

DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS issues;
DROP TABLE IF EXISTS statuses;
DROP TABLE IF EXISTS priorities;
DROP TABLE IF EXISTS issue_types;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS projects;

CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_key VARCHAR(10) UNIQUE NOT NULL,
    project_name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE issue_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE priorities (
    priority_id INT AUTO_INCREMENT PRIMARY KEY,
    priority_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE statuses (
    status_id INT AUTO_INCREMENT PRIMARY KEY,
    status_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE issues (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    issue_key VARCHAR(20) UNIQUE NOT NULL,
    project_id INT NOT NULL,
    type_id INT NOT NULL,
    priority_id INT NOT NULL,
    status_id INT NOT NULL,
    summary VARCHAR(255) NOT NULL,
    description TEXT,
    assignee_id INT,
    reporter_id INT NOT NULL,
    created_date DATETIME NOT NULL,
    updated_date DATETIME NOT NULL,
    due_date DATE,
    resolution TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (type_id) REFERENCES issue_types(type_id),
    FOREIGN KEY (priority_id) REFERENCES priorities(priority_id),
    FOREIGN KEY (status_id) REFERENCES statuses(status_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (reporter_id) REFERENCES users(user_id)
);

CREATE TABLE comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT NOT NULL,
    author_id INT NOT NULL,
    comment_text TEXT NOT NULL,
    created_date DATETIME NOT NULL,
    FOREIGN KEY (issue_id) REFERENCES issues(issue_id),
    FOREIGN KEY (author_id) REFERENCES users(user_id)
);

-- Indexes for common queries
CREATE INDEX idx_issues_status ON issues(status_id);
CREATE INDEX idx_issues_assignee ON issues(assignee_id);
CREATE INDEX idx_issues_project ON issues(project_id);
CREATE INDEX idx_issues_created ON issues(created_date);
CREATE INDEX idx_comments_issue ON comments(issue_id);