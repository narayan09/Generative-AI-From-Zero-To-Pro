# Jira User Guide – Complete Reference

## 1. Introduction to Jira
Jira is a powerful issue‑tracking and project‑management tool developed by Atlassian. It allows teams to plan, track, and release software, manage service desks, and more.

### 1.1 Key Concepts
- **Project**: A container for issues. Projects have a unique key (e.g., PROJ).
- **Issue**: A single work item – could be a bug, task, story, or epic.
- **Board**: A visual representation of a project’s workflow (Scrum or Kanban).
- **Sprint**: A fixed time period (usually 1‑4 weeks) during which a Scrum team works on a set of issues.

## 2. Navigating Jira
### 2.1 Dashboard
Your personal dashboard shows gadgets like “Assigned to Me”, “My Open Issues”, and activity streams.

### 2.2 Search and JQL
Jira’s powerful search uses JQL (Jira Query Language). Examples:
- `project = ALPHA AND status = Open`
- `assignee = currentUser() AND priority = Blocker`
- `due < now() AND status not in (Resolved, Closed)`

### 2.3 Filters
Save your frequent searches as filters for easy access.

## 3. Working with Issues
### 3.1 Creating an Issue
1. Click **Create** in the top menu.
2. Select the project and issue type.
3. Fill in the summary, description, priority, and other fields.
4. Assign the issue if needed.
5. Click **Create**.

### 3.2 Viewing and Editing Issues
- The issue detail view shows all fields, attachments, comments, and history.
- You can edit fields inline or by clicking the edit button.

### 3.3 Assigning and Reassigning
Click the **Assignee** field and search for a user. Only users with project permissions appear.

### 3.4 Comments and Mentions
- In the issue view, scroll to **Activity** → **Comment**.
- Use `@username` to mention someone; they’ll get a notification.

### 3.5 Transitions and Workflow
- Move an issue through statuses by clicking buttons like “Start Progress”, “Resolve”, or “Close”.
- The available transitions depend on the project’s workflow.

## 4. Scrum in Jira
### 4.1 Backlog Management
The backlog contains all unplanned issues. You can prioritise by dragging and dropping.

### 4.2 Sprint Planning
1. Go to the Backlog tab.
2. Click **Create Sprint**.
3. Drag issues into the sprint.
4. Click **Start Sprint** and set the duration.

### 4.3 Active Sprint
During a sprint, track progress on the **Active Sprint** board. Move issues from To Do → In Progress → Done.

### 4.4 Sprint Retrospective
Use Jira’s reports (Burndown Chart, Sprint Report) to review team performance.

## 5. Kanban in Jira
- A Kanban board visualises continuous workflow.
- Columns represent statuses; issues flow from left to right.
- Work In Progress (WIP) limits can be set to avoid bottlenecks.

## 6. Reports and Dashboards
- **Burndown Chart**: Shows remaining work over time.
- **Velocity Chart**: Average completed story points per sprint.
- **Created vs Resolved**: Trend of issue creation versus resolution.
- You can add gadgets to dashboards for a custom view.

## 7. Notifications and Watchers
- You receive notifications for issues you are watching, assigned to, or mentioned in.
- Click the **eye icon** on an issue to become a watcher.

## 8. Keyboard Shortcuts
- `c` – Create new issue
- `i` – Assign to me
- `g + d` – Go to dashboard
- `g + b` – Go to boards

## 9. Mobile App
Jira’s mobile app (iOS/Android) allows you to view, update, and comment on issues on the go.

## 10. Tips & Best Practices
- Keep summaries short and descriptive.
- Update issue status regularly.
- Use labels and components for better filtering.
- Write clear bug reports with steps to reproduce, expected vs actual results.