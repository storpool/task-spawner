from redis.sentinel import Sentinel
import redis
import logging

class RedisClient:
    def __init__(self, config):
        if config.get("REDIS_USE_SENTINEL"):
            if not config.get("REDIS_SENTINEL_HOSTS"):
                raise ValueError("Sentinel hosts must be provided if using Redis Sentinel")

            sentinel_hosts = [
                tuple(host.split(":")) if ":" in host else (host, 26379)
                for host in config["REDIS_SENTINEL_HOSTS"].split(",")
            ]
            sentinel_hosts = [(h, int(p)) for h, p in sentinel_hosts]

            sentinel = Sentinel(sentinel_hosts, socket_timeout=2)
            self.client = sentinel.master_for(
                config["REDIS_SENTINEL_MASTER"],
                db=int(config.get("REDIS_DB", 0)),
                decode_responses=True
            )

            logging.info("Connected to Redis via Sentinel")
        else:
            self.client = redis.Redis(
                host=config["REDIS_HOST"],
                port=config["REDIS_PORT"],
                db=config["REDIS_DB"],
                decode_responses=True
            )
            logging.info("Connected to Redis directly")

    def map_ticket_to_task(self, ticket_id, task_id):
        self.client.hset("ticket_task_map", ticket_id, task_id)

    def get_task_by_ticket(self, ticket_id):
        return self.client.hget("ticket_task_map", ticket_id)

    def delete_ticket_task(self, ticket_id):
        self.client.hdel("ticket_task_map", ticket_id)

    def set_user_mapping(self, zendesk_user_id, teamwork_user_id):
        self.client.hset("user_map", zendesk_user_id, teamwork_user_id)

    def get_teamwork_user(self, zendesk_user_id):
        return self.client.hget("user_map", zendesk_user_id)

    def delete_user_mapping(self, zendesk_user_id):
        self.client.hdel("user_map", zendesk_user_id)
