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

## Helm Deployment Instructions

This application can be deployed using the provided Helm chart under `charts/ticket-spawner`.

### Set Required Values

Before installing the chart, you must provide sensitive credentials and configuration values. These are stored as a Kubernetes `Secret`.

Create a custom `values.yaml` file (e.g., `my-values.yaml`) with:

```yaml
secrets:
  zendeskSubdomain: your-zendesk-subdomain
  zendeskApiToken: your-base64-encoded-zendesk-api-token
  teamworkDomain: your-teamwork-domain
  teamworkApiToken: your-base64-encoded-teamwork-api-token
  teamworkProjectId: your-teamwork-project-id

ingress:
  fqdn: ticket-spawner.yourdomain.com
  tlsSecretName: ticket-spawner-tls
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
```

> **Note**: `zendeskApiToken` and `teamworkApiToken` must be base64-encoded, as they are inserted directly into a Kubernetes `Secret`.

### Install with Helm

```bash
helm upgrade --install ticket-spawner charts/ticket-spawner \
  --namespace ticket-spawner --create-namespace \
  -f my-values.yaml
```

This will:

- Deploy the application with 2 replicas.
- Deploy a Bitnami Redis Sentinel cluster.
- Configure a Kubernetes Ingress.
- Automatically issue a TLS certificate using CertManager.

### Access the App

Once deployed, your app will be accessible at the FQDN you specified (e.g., `https://ticket-spawner.yourdomain.com`), with TLS handled by CertManager.

### Optional Settings

| Setting                        | Description                                   | Default            |
|-------------------------------|-----------------------------------------------|--------------------|
| `ingress.enabled`             | Enable ingress resource                       | `true`             |
| `ingress.tlsEnabled`          | Enable TLS for ingress                        | `true`             |
| `replicaCount`                | Number of application pods                    | `2`                |
| `env.redisSentinelMaster`     | Redis Sentinel master name                    | `mymaster`         |

## License

This project is open source and available under the MIT License.