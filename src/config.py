import os
import sys
import argparse
import logging


def get_config():
    parser = argparse.ArgumentParser(description="Zendesk → Teamwork Sync Service")

    parser.add_argument("--zendesk-subdomain", help="Zendesk subdomain")
    parser.add_argument("--zendesk-api-token", help="Zendesk API token")
    parser.add_argument("--teamwork-domain", help="Teamwork domain")
    parser.add_argument("--teamwork-api-token", help="Teamwork API token")
    parser.add_argument("--teamwork-project-id", help="Teamwork project ID")
    parser.add_argument("--webhook-secret", help="Secret to authenticate incoming webhooks")

    args, _ = parser.parse_known_args()

    config = {
        "ZENDESK_SUBDOMAIN": os.getenv("ZENDESK_SUBDOMAIN", args.zendesk_subdomain),
        "ZENDESK_API_TOKEN": os.getenv("ZENDESK_API_TOKEN", args.zendesk_api_token),
        "TEAMWORK_DOMAIN": os.getenv("TEAMWORK_DOMAIN", args.teamwork_domain),
        "TEAMWORK_API_TOKEN": os.getenv("TEAMWORK_API_TOKEN", args.teamwork_api_token),
        "TEAMWORK_PROJECT_ID": os.getenv("TEAMWORK_PROJECT_ID", args.teamwork_project_id),
        "WEBHOOK_SECRET": os.getenv("ZENDESK_WEBHOOK_SECRET", args.webhook_secret),
    }

    required_keys = [
        "ZENDESK_SUBDOMAIN",
        "ZENDESK_API_TOKEN",
        "TEAMWORK_DOMAIN",
        "TEAMWORK_API_TOKEN",
        "TEAMWORK_PROJECT_ID",
        "WEBHOOK_SECRET"
    ]

    for key in required_keys:
        if not config[key]:
            logging.critical(f"Missing required configuration: {key}")
            sys.exit(1)

    return config
