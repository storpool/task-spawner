# Zendesk to Teamwork Synchronization Service

This application listens for Zendesk ticket events and synchronizes them with Teamwork tasks. All mapping and state are stored using Zendesk metadata. Redis is no longer used.

## Features

- **Task Creation**: Creates a Teamwork task when a new Zendesk ticket is created and contains the `teamwork_task` tag.
- **Task Title**: Tasks are named using the pattern `[Ticket #1234] ticket title`.
- **Assignee Mapping**: Tasks are assigned to the Teamwork user based on the Zendesk agent’s `teamwork_user_id` custom field.
- **Task List**: Tasks are created in a configured Teamwork task list.
- **Tag-based Sync**:
  - If the `teamwork_task` tag is removed, task updates are paused.
  - If the tag is re-added and the user has a `teamwork_user_id`, sync resumes.
- **Status Sync**:
  - `solved` → mark task complete
  - `reopened` / `open` → mark task incomplete
  - `closed` / `deleted` → delete the task
  - `merged` → mark task complete and append `Merged into ticket #number` to the description
- **Agent Mapping**: The application automatically maps Zendesk agents to Teamwork users by matching email addresses and writes the Teamwork user ID into the agent’s `teamwork_user_id` custom field.
- **Metadata Storage**:
  - Task ID is stored in `teamwork_task_id` custom field on the ticket.
  - All required Zendesk custom fields are created automatically.

## Configuration

The app is configured via command-line arguments or environment variables.

| Description              | CLI Argument                     | Env Var                     | Required |
|--------------------------|----------------------------------|-----------------------------|----------|
| Zendesk subdomain        | `--zendesk-subdomain`            | `ZENDESK_SUBDOMAIN`         | ✅       |
| Zendesk API token        | `--zendesk-api-token`            | `ZENDESK_API_TOKEN`         | ✅       |
| Teamwork domain          | `--teamwork-domain`              | `TEAMWORK_DOMAIN`           | ✅       |
| Teamwork API token       | `--teamwork-api-token`           | `TEAMWORK_API_TOKEN`        | ✅       |
| Teamwork project ID      | `--teamwork-project-id`          | `TEAMWORK_PROJECT_ID`       | ✅       |
| Teamwork task list ID    | `--teamwork-task-list-id`        | `TEAMWORK_TASK_LIST_ID`     | ✅       |

## How It Works

1. On startup, the app ensures the following custom fields exist in Zendesk:
   - Ticket custom field: `teamwork_task_id`
   - User custom field: `teamwork_user_id`

2. When a ticket is created or updated:
   - If the `teamwork_task` tag is present:
     - A task is created in Teamwork if it doesn't already exist.
     - The task is assigned to the Zendesk agent’s mapped Teamwork user.
     - The task ID is stored in the Zendesk ticket’s `teamwork_task_id` field.
   - If the tag is removed, no updates are made to the task.
   - If the tag is re-added and mapping exists, updates resume.

3. Ticket status drives task state:
   - `solved` → task completed
   - `reopened` → task reopened
   - `closed` or deleted → task deleted
   - `merged` → task marked complete, description updated

## Running the App

Install Python dependencies:

```bash
pip install -r requirements.txt
