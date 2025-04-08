import argparse
import os

def get_config():
    parser = argparse.ArgumentParser(description="Zendesk → Teamwork Sync Service")

    parser.add_argument("--zendesk-subdomain", default=None, help="Zendesk subdomain")
    parser.add_argument("--zendesk-api-token", default=None, help="Zendesk API token")
    parser.add_argument("--teamwork-domain", default=None, help="Teamwork domain")
    parser.add_argument("--teamwork-api-token", default=None, help="Teamwork API token")
    parser.add_argument("--teamwork-project-id", default=None, help="Teamwork project ID")
    parser.add_argument("--redis-host", default="localhost", help="Redis host")
    parser.add_argument("--redis-port", default=6379, type=int, help="Redis port")
    parser.add_argument("--redis-db", default=0, type=int, help="Redis database")
    parser.add_argument("--redis-use-sentinel", action="store_true", help="Use Redis Sentinel for HA")
    parser.add_argument("--redis-sentinel-hosts", default=None,
                        help="Comma-separated list of Sentinel hosts (host1:port,host2:port)")
    parser.add_argument("--redis-sentinel-master", default="mymaster", help="Redis Sentinel master name")

    args, _ = parser.parse_known_args()

    config = {
        "ZENDESK_SUBDOMAIN": os.environ.get("ZENDESK_SUBDOMAIN", args.zendesk_subdomain),
        "ZENDESK_API_TOKEN": os.environ.get("ZENDESK_API_TOKEN", args.zendesk_api_token),
        "TEAMWORK_DOMAIN": os.environ.get("TEAMWORK_DOMAIN", args.teamwork_domain),
        "TEAMWORK_API_TOKEN": os.environ.get("TEAMWORK_API_TOKEN", args.teamwork_api_token),
        "TEAMWORK_PROJECT_ID": os.environ.get("TEAMWORK_PROJECT_ID", args.teamwork_project_id),
        "REDIS_HOST": os.environ.get("REDIS_HOST", args.redis_host),
        "REDIS_PORT": int(os.environ.get("REDIS_PORT", args.redis_port)),
        "REDIS_DB": int(os.environ.get("REDIS_DB", args.redis_db)),
        "REDIS_USE_SENTINEL": os.environ.get("REDIS_USE_SENTINEL", str(args.redis_use_sentinel)).lower() in (
        "1", "true", "yes"),
        "REDIS_SENTINEL_HOSTS": os.environ.get("REDIS_SENTINEL_HOSTS", args.redis_sentinel_hosts),
        "REDIS_SENTINEL_MASTER": os.environ.get("REDIS_SENTINEL_MASTER", args.redis_sentinel_master),

    }

    # Basic validation
    required_keys = ["ZENDESK_SUBDOMAIN", "ZENDESK_API_TOKEN", "TEAMWORK_DOMAIN", "TEAMWORK_API_TOKEN", "TEAMWORK_PROJECT_ID"]
    for key in required_keys:
        if not config[key]:
            raise ValueError(f"Missing required configuration: {key}")

    return config
