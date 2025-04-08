# Zendesk to Teamwork Synchronization Service

This is a Python Flask application that listens to Zendesk ticket events and synchronizes them with Teamwork tasks. It is built for Kubernetes and deployed via Helm. Configuration is split between a generated `config.toml` file and secrets stored in Kubernetes Secrets.

## Features

- Creates a Teamwork task when a Zendesk ticket is created
- Assigns the task to the Zendesk agent if a valid mapping exists
- Updates task title and assignee on ticket updates
- Synchronizes ticket lifecycle to task status:
  - Solved → complete task
  - Reopened → mark task incomplete
  - Closed or deleted → delete task
  - Merged → mark task complete
- Validates the Teamwork task list at startup
- Webhook secured using a secret header
- All Zendesk API interactions use **Basic Auth with API token**

---

## Configuration Overview

### Configuration is split into:

1. A `config.toml` file rendered from Helm values:
    - Includes non-sensitive values like domains and IDs
2. A Kubernetes Secret:
    - Stores API tokens and the webhook secret

---

## config.toml Format

The following TOML file is generated automatically by Helm and mounted into the container:

```toml
[zendesk]
subdomain = "your-subdomain"

[teamwork]
domain = "your-teamwork-domain"
project_id = "123456"
task_list = "654321"
