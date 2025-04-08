import argparse
import os

def get_config():
    parser = argparse.ArgumentParser(description="Zendesk → Teamwork Sync Service")

    parser.add_argument("--zendesk-subdomain", required=True)
    parser.add_argument("--zendesk-api-token", required=True)
    parser.add_argument("--teamwork-domain", required=True)
    parser.add_argument("--teamwork-api-token", required=True)
    parser.add_argument("--teamwork-project-id", required=True)
    parser.add_argument("--teamwork-task-list-id", required=True)

    args, _ = parser.parse_known_args()

    config = {
        "ZENDESK_SUBDOMAIN": os.environ.get("ZENDESK_SUBDOMAIN", args.zendesk_subdomain),
        "ZENDESK_API_TOKEN": os.environ.get("ZENDESK_API_TOKEN", args.zendesk_api_token),
        "TEAMWORK_DOMAIN": os.environ.get("TEAMWORK_DOMAIN", args.teamwork_domain),
        "TEAMWORK_API_TOKEN": os.environ.get("TEAMWORK_API_TOKEN", args.teamwork_api_token),
        "TEAMWORK_PROJECT_ID": os.environ.get("TEAMWORK_PROJECT_ID", args.teamwork_project_id),
        "TEAMWORK_TASK_LIST_ID": os.environ.get("TEAMWORK_TASK_LIST_ID", args.teamwork_task_list_id),
    }

    return config
