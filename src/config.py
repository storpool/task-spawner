import os
import sys
import argparse
import logging

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Python <3.11

def get_config():
    parser = argparse.ArgumentParser(description="Zendesk → Teamwork Sync Service")

    parser.add_argument("--config-file", default="config.toml", help="Path to TOML config file")
    parser.add_argument("--zendesk-api-token", help="Zendesk API token")
    parser.add_argument("--teamwork-api-token", help="Teamwork API token")
    parser.add_argument("--webhook-secret", help="Secret to authenticate incoming webhooks")

    args, _ = parser.parse_known_args()

    try:
        with open(args.config_file, "rb") as f:
            toml_data = tomllib.load(f)
    except FileNotFoundError:
        logging.critical(f"Configuration file not found: {args.config_file}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Error loading config file: {e}")
        sys.exit(1)

    config = {
        "ZENDESK_SUBDOMAIN": toml_data.get("zendesk", {}).get("subdomain"),
        "ZENDESK_API_TOKEN": os.getenv("ZENDESK_API_TOKEN", args.zendesk_api_token),
        "TEAMWORK_DOMAIN": toml_data.get("teamwork", {}).get("domain"),
        "TEAMWORK_API_TOKEN": os.getenv("TEAMWORK_API_TOKEN", args.teamwork_api_token),
        "TEAMWORK_PROJECT_ID": toml_data.get("teamwork", {}).get("project_id"),
        "TEAMWORK_TASK_LIST": toml_data.get("teamwork", {}).get("task_list"),
        "WEBHOOK_SECRET": os.getenv("ZENDESK_WEBHOOK_SECRET", args.webhook_secret),
    }

    required_keys = [
        "ZENDESK_SUBDOMAIN",
        "ZENDESK_API_TOKEN",
        "TEAMWORK_DOMAIN",
        "TEAMWORK_API_TOKEN",
        "TEAMWORK_PROJECT_ID",
        "TEAMWORK_TASK_LIST",
        "WEBHOOK_SECRET"
    ]

    for key in required_keys:
        if not config[key]:
            logging.critical(f"Missing required configuration: {key}")
            sys.exit(1)

    return config
