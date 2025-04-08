import requests
from requests.auth import HTTPBasicAuth

def get_auth(config):
    email = config["ZENDESK_EMAIL"]
    token = config["ZENDESK_API_TOKEN"]
    return HTTPBasicAuth(f"{email}/token", token)

def ensure_custom_fields(config):
    fields = get_ticket_fields(config)
    if not any(f["title"] == "teamwork_task_id" for f in fields):
        create_ticket_field(config, "teamwork_task_id")

    users_fields = get_user_fields(config)
    if not any(f["key"] == "teamwork_user_id" for f in users_fields):
        create_user_field(config, "teamwork_user_id")

def get_ticket_fields(config):
    url = f"https://{config['ZENDESK_SUBDOMAIN']}.zendesk.com/api/v2/ticket_fields.json"
    return requests.get(url, auth=get_auth(config)).json()["ticket_fields"]

def get_user_fields(config):
    url = f"https://{config['ZENDESK_SUBDOMAIN']}.zendesk.com/api/v2/user_fields.json"
    return requests.get(url, auth=get_auth(config)).json()["user_fields"]

def create_ticket_field(config, name):
    url = f"https://{config['ZENDESK_SUBDOMAIN']}.zendesk.com/api/v2/ticket_fields.json"
    payload = {
        "ticket_field": {
            "type": "text",
            "title": name,
            "key": name,
            "required": False
        }
    }
    requests.post(url, auth=get_auth(config), json=payload)

def create_user_field(config, name):
    url = f"https://{config['ZENDESK_SUBDOMAIN']}.zendesk.com/api/v2/user_fields.json"
    payload = {
        "user_field": {
            "type": "text",
            "title": name,
            "key": name
        }
    }
    requests.post(url, auth=get_auth(config), json=payload)

def get_teamwork_user_id(agent_id, config):
    user_url = f"https://{config['ZENDESK_SUBDOMAIN']}.zendesk.com/api/v2/users/{agent_id}.json"
    res = requests.get(user_url, auth=get_auth(config)).json()
    user = res["user"]
    user_fields = user.get("user_fields", {})

    if "teamwork_user_id" in user_fields and user_fields["teamwork_user_id"]:
        return user_fields["teamwork_user_id"]

    # Lookup by email
    email = user["email"]
    tw_id = find_teamwork_user_id_by_email(email, config)

    # Store back in Zendesk
    if tw_id:
        set_teamwork_user_id(agent_id, tw_id, config)

    return tw_id

def set_teamwork_user_id(agent_id, teamwork_id, config):
    url = f"https://{config['ZENDESK_SUBDOMAIN']}.zendesk.com/api/v2/users/{agent_id}.json"
    payload = {
        "user": {
            "user_fields": {
                "teamwork_user_id": teamwork_id
            }
        }
    }
    requests.put(url, auth=get_auth(config), json=payload)

def find_teamwork_user_id_by_email(email, config):
    url = f"https://{config['TEAMWORK_DOMAIN']}.teamwork.com/people.json"
    headers = {
        "Authorization": f"Bearer {config['TEAMWORK_API_TOKEN']}"
    }
    people = requests.get(url, headers=headers).json()["people"]
    for person in people:
        if person["email"].lower() == email.lower():
            return str(person["id"])
    return None

def get_ticket_task_id(ticket, config):
    for f in ticket.get("custom_fields", []):
        if f["id"] and f["id"] == get_task_id_field_id(config):
            return f["value"]
    return None

def set_ticket_task_id(ticket_id, task_id, config):
    task_field_id = get_task_id_field_id(config)
    url = f"https://{config['ZENDESK_SUBDOMAIN']}.zendesk.com/api/v2/tickets/{ticket_id}.json"
    payload = {
        "ticket": {
            "custom_fields": [
                {
                    "id": task_field_id,
                    "value": task_id
                }
            ]
        }
    }
    requests.put(url, auth=get_auth(config), json=payload)

def get_task_id_field_id(config):
    fields = get_ticket_fields(config)
    for field in fields:
        if field["key"] == "teamwork_task_id":
            return field["id"]
    raise Exception("Custom field 'teamwork_task_id' not found.")
