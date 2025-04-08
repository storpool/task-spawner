import argparse
from config import get_config
from redis_client import RedisClient

def add_mapping(redis_client, zendesk_user_id, teamwork_user_id):
    redis_client.set_user_mapping(zendesk_user_id, teamwork_user_id)
    print(f"Mapped Zendesk user {zendesk_user_id} to Teamwork user {teamwork_user_id}")

def remove_mapping(redis_client, zendesk_user_id):
    redis_client.delete_user_mapping(zendesk_user_id)
    print(f"Removed mapping for Zendesk user {zendesk_user_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Admin CLI for user mappings")
    subparsers = parser.add_subparsers(dest="command")

    add_cmd = subparsers.add_parser("add")
    add_cmd.add_argument("zendesk_user_id")
    add_cmd.add_argument("teamwork_user_id")

    rm_cmd = subparsers.add_parser("remove")
    rm_cmd.add_argument("zendesk_user_id")

    args = parser.parse_args()
    config = get_config()
    redis = RedisClient(config)

    if args.command == "add":
        add_mapping(redis, args.zendesk_user_id, args.teamwork_user_id)
    elif args.command == "remove":
        remove_mapping(redis, args.zendesk_user_id)
    else:
        parser.print_help()
