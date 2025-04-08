# Zendesk to Teamwork Synchronization Service

This is a Python Flask application that listens to Zendesk ticket events and synchronizes them with Teamwork tasks. It is designed for use in containerized environments and supports Redis Sentinel for high availability.

## Features

- Creates a new Teamwork task when a new Zendesk ticket is created.
- Assigns the task to the Zendesk agent who opened the ticket, if a user mapping exists.
- If no agent mapping exists, the task is created with no assignee ("Anyone").
- Updates the task title if the ticket title changes.
- Updates the task assignee if the ticket is assigned or reassigned.
- Tracks the status of the ticket:
  - When a ticket is marked as **solved**, the Teamwork task is marked as complete.
  - When a ticket is **reopened**, the task is marked as incomplete.
  - When a ticket is **closed** or **deleted**, the task is deleted.
  - When a ticket is **merged**, the task is marked as complete.
- Stores ticket-to-task and user ID mappings in Redis.
- Provides a CLI to manage user mappings.
- Exposes a `/healthz` endpoint for readiness and liveness checks.
- Can be run with direct Redis or Redis Sentinel.

## Configuration

The application accepts both command-line arguments and environment variables for configuration. Environment variables take precedence.

### Required Configuration

| Description                | CLI Argument                      | Environment Variable           |
|----------------------------|-----------------------------------|--------------------------------|
| Zendesk subdomain          | `--zendesk-subdomain`             | `ZENDESK_SUBDOMAIN`            |
| Zendesk API token          | `--zendesk-api-token`             | `ZENDESK_API_TOKEN`            |
| Teamwork domain            | `--teamwork-domain`               | `TEAMWORK_DOMAIN`              |
| Teamwork API token         | `--teamwork-api-token`            | `TEAMWORK_API_TOKEN`           |
| Teamwork project ID        | `--teamwork-project-id`           | `TEAMWORK_PROJECT_ID`          |

### Redis Configuration (Standalone)

| Description        | CLI Argument           | Environment Variable   | Default    |
|--------------------|------------------------|-------------------------|------------|
| Redis host         | `--redis-host`         | `REDIS_HOST`            | `localhost`|
| Redis port         | `--redis-port`         | `REDIS_PORT`            | `6379`     |
| Redis database     | `--redis-db`           | `REDIS_DB`              | `0`        |

### Redis Configuration (Sentinel Mode)

| Description              | CLI Argument                  | Environment Variable           | Default     |
|--------------------------|-------------------------------|----------------------------------|-------------|
| Use Redis Sentinel       | `--redis-use-sentinel`        | `REDIS_USE_SENTINEL`             | false       |
| Sentinel hosts           | `--redis-sentinel-hosts`      | `REDIS_SENTINEL_HOSTS`           |             |
| Sentinel master name     | `--redis-sentinel-master`     | `REDIS_SENTINEL_MASTER`          | `mymaster`  |

## Running the Application

Example using CLI and environment variables:

```bash
export ZENDESK_API_TOKEN=your_zendesk_token
export TEAMWORK_API_TOKEN=your_teamwork_token

python run.py \
  --zendesk-subdomain=mycompany \
  --teamwork-domain=myteam \
  --teamwork-project-id=987654 \
  --redis-use-sentinel \
  --redis-sentinel-hosts=redis-0:26379,redis-1:26379 \
  --redis-sentinel-master=mymaster
