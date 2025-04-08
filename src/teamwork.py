import requests
import logging
from requests.auth import HTTPBasicAuth


def get_auth(config):
    """Use Teamwork API token as username with Basic Auth (v1 API)."""
    return HTTPBasicAuth(config["TEAMWORK_API_TOKEN"], "x")


def get_base_url(config):
    return f"https://{config['TEAMWORK_DOMAIN']}.teamwork.com"


def create_task(title, ticket_number, teamwork_user_id, config):
    url = f"{get_base_url(config)}/tasklists/{config['TEAMWORK_TASK_LIST']}/tasks.json"
    payload = {
        "todo-item": {
            "content": f"[Ticket #{ticket_number}] {title}",
        }
    }

    if teamwork_user_id:
        payload["todo-item"]["responsible-party-id"] = teamwork_user_id

    response = requests.post(url, json=payload, auth=get_auth(config))
    response.raise_for_status()
    task_id = response.json()["todo-item"]["id"]
    logging.info(f"Created Teamwork task {task_id} in list {config['TEAMWORK_TASK_LIST']}")
    return task_id


def update_task_title(task_id, new_title, config):
    url = f"{get_base_url(config)}/tasks/{task_id}.json"
    payload = {
        "todo-item": {
            "content": new_title
        }
    }
    response = requests.put(url, json=payload, auth=get_auth(config))
    response.raise_for_status()
    logging.info(f"Updated Teamwork task {task_id} title")


def update_task_assignee(task_id, teamwork_user_id, config):
    url = f"{get_base_url(config)}/tasks/{task_id}.json"
    payload = {
        "todo-item": {
            "responsible-party-id": teamwork_user_id if teamwork_user_id else ""
        }
    }
    response = requests.put(url, json=payload, auth=get_auth(config))
    response.raise_for_status()
    logging.info(f"Updated Teamwork task {task_id} assignee")


def complete_task(task_id, config):
    url = f"{get_base_url(config)}/tasks/{task_id}/complete.json"
    response = requests.put(url, auth=get_auth(config))
    response.raise_for_status()
    logging.info(f"Marked Teamwork task {task_id} complete")


def reopen_task(task_id, config):
    url = f"{get_base_url(config)}/tasks/{task_id}/uncomplete.json"
    response = requests.put(url, auth=get_auth(config))
    response.raise_for_status()
    logging.info(f"Reopened Teamwork task {task_id}")


def delete_task(task_id, config):
    url = f"{get_base_url(config)}/tasks/{task_id}.json"
    response = requests.delete(url, auth=get_auth(config))
    if response.status_code == 404:
        logging.warning(f"Teamwork task {task_id} already deleted")
        return
    response.raise_for_status()
    logging.info(f"Deleted Teamwork task {task_id}")


def get_task_details(task_id, config):
    url = f"{get_base_url(config)}/tasks/{task_id}.json"
    response = requests.get(url, auth=get_auth(config))
    response.raise_for_status()
    return response.json()["todo-item"]


def append_to_task_description(task_id, text, config):
    task = get_task_details(task_id, config)
    description = task.get("description", "") or ""
    new_description = description + "\n\n" + text

    url = f"{get_base_url(config)}/tasks/{task_id}.json"
    payload = {
        "todo-item": {
            "description": new_description
        }
    }
    response = requests.put(url, json=payload, auth=get_auth(config))
    response.raise_for_status()
    logging.info(f"Updated Teamwork task {task_id} description")
