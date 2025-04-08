import argparse
import os
import requests

def get_config():
    return {
        "ZENDESK_SUBDOMAIN": os.environ["ZENDESK_SUBDOMAIN"],
        "ZENDESK_API_TOKEN": os.environ["ZENDESK_API_TOKEN"]
    }

def set_teamwork_user_id(zendesk_user_id, teamwork_user_id, config):
    url = f"https://{config['ZENDESK_SUBDOMAIN']}.zendesk.com/api/v2/users/{zendesk_user_id}.json"
    headers = {
        "Authorization": f"Bearer {config['ZENDESK_API_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "user": {
            "user_fields": {
                "teamwork_user_id": teamwork_user_id
            }
        }
    }
    response = requests.put(url, headers=headers, json=payload)
    response.raise_for_status()
    print(f"Mapped Zendesk user {zendesk_user_id} to Teamwork user {teamwork_user_id}")

def remove_teamwork_user_id(zendesk_user_id, config):
    set_teamwork_user_id(zendesk_user_id, None, config)
    print(f"Removed Teamwork user mapping for Zendesk user {zendesk_user_id}")

def main():
    parser = argparse.ArgumentParser(description="Admin CLI for Zendesk-Teamwork user mappings")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_cmd = subparsers.add_parser("add")
    add_cmd.add_argument("zendesk_user_id")
    add_cmd.add_argument("teamwork_user_id")

    rm_cmd = subparsers.add_parser("remove")
    rm_cmd.add_argument("zendesk_user_id")

    args = parser.parse_args()
    config = get_config()

    if args.command == "add":
        set_teamwork_user_id(args.zendesk_user_id, args.teamwork_user_id, config)
    elif args.command == "remove":
        remove_teamwork_user_id(args.zendesk_user_id, config)

if __name__ == "__main__":
    main()
