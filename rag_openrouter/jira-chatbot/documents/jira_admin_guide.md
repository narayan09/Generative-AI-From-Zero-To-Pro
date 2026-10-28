# Jira Administration Guide

## 1. Overview
This guide covers administration of Jira Cloud and Data Center – user management, project setup, workflows, permissions, and customisation.

## 2. User Management
### 2.1 Adding Users
1. Navigate to **Administration** (cog icon) → **User management**.
2. Click **Invite users**.
3. Enter email addresses and assign them to groups.
4. Set product access (Jira Software, Confluence, etc.).

### 2.2 Groups and Permissions
- **Groups** (e.g., `jira-software-users`, `administrators`) simplify permission management.
- **Project roles** (e.g., Administrators, Developers, Viewers) map users/groups to project-specific permissions.

### 2.3 Global Permissions
Control who can:
- Administer Jira (global admin)
- Browse users and groups
- Create shared objects (filters, dashboards)

## 3. Project Configuration
### 3.1 Creating a Project
1. Go to **Projects** → **Create project**.
2. Choose a template (Scrum, Kanban, Bug tracking, etc.).
3. Set the project name, key, and lead.

### 3.2 Project Settings
- **Issue types**: Define which types are available (Bug, Task, Story, Epic, Sub-task).
- **Workflows**: Select or create a workflow.
- **Screens**: Customise which fields appear on create/edit/view screens.
- **Fields**: Add custom fields (text, date, dropdown, etc.).
- **Permissions**: Grant project permissions to roles.

### 3.3 Components and Versions
- **Components** represent sub‑sections of a project (e.g., “Backend”, “Frontend”). They help group issues.
- **Versions** track releases. You can set start/release dates and manage issues per version.

## 4. Workflows
### 4.1 Workflow Structure
A workflow consists of **statuses** and **transitions**.
- **Statuses**: Open, In Progress, Resolved, Closed, etc.
- **Transitions**: Links between statuses (e.g., “Start Progress” → In Progress).

### 4.2 Editing Workflows
- Go to **Issues** → **Workflows**.
- Edit an existing workflow or create a new one.
- Use the diagram mode to drag and drop transitions.

### 4.3 Conditions, Validators, and Post Functions
- **Conditions**: Who can execute a transition (e.g., only assignee).
- **Validators**: Check data before transition (e.g., comment required).
- **Post functions**: Automatic actions after transition (e.g., assign to reporter, re‑index issue).

### 4.4 Workflow Schemes
Associate a workflow with an issue type by using workflow schemes. One project can have different workflows for bugs, tasks, etc.

## 5. Permissions Deep Dive
### 5.1 Project Permissions
Important permissions:
- **Browse Projects**: View issues within a project.
- **Create Issues**: Create new issues.
- **Edit Issues**: Modify issue fields (may be restricted by issue security).
- **Assign Issues**: Assign an issue to a user.
- **Resolve Issues**: Move issues to a resolved status.
- **Delete Issues**: Delete issues (use with caution).

### 5.2 Issue Security Levels
- Restrict issue visibility based on security levels.
- Users can only see issues if they have permission for that security level.

## 6. Customisation
### 6.1 Custom Fields
Add fields like:
- Text (single/multi line)
- Select list (single/multiple)
- Date/date time
- User picker
- Labels (multi-select tags)

### 6.2 Screen Schemes
- **Create screen** – fields shown when creating an issue.
- **Edit screen** – fields shown when editing.
- **View screen** – fields shown in issue view.

### 6.3 Field Configuration
- Show/hide fields, set them as required or optional.
- Customise per issue type.

## 7. Automation
Jira Automation (built‑in rule engine) allows:
- Automatically assigning issues based on conditions.
- Sending notifications on status changes.
- Closing parent issues when all subtasks are done.
- Syncing with external systems via webhooks.

## 8. Integrations
- **Confluence**: Link issues to documentation.
- **Bitbucket/GitHub**: View commits and branches associated with issues.
- **Slack/Teams**: Receive notifications.
- **REST API**: Build custom integrations.

## 9. Data Management & Backup
- Use **Backup Manager** to create backups (Jira Cloud: 48‑hour auto backup; Data Center: manual).
- For Data Center, schedule regular XML backups.

## 10. Security Best Practices
- Enforce two‑factor authentication.
- Limit global administrator accounts.
- Use API tokens for integrations.
- Regularly review user access.

---

*For further information, refer to the official [Atlassian documentation](https://confluence.atlassian.com/jira).*