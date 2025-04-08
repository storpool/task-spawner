import requests
import logging

def get_headers(config):
    return {
        "Authorization": f"Bearer {config['TEAMWORK_API_TOKEN']}",
        "Content-Type": "application/json"
    }

def validate_task_list_exists(config):
    url = f"https://{config['TEAMWORK_DOMAIN']}.teamwork.com/tasklists/{config['TEAMWORK_TASK_LIST']}.json"
    response = requests.get(url, headers=get_headers(config))

    if response.status_code == 404:
        logging.critical(f"Teamwork task list {config['TEAMWORK_TASK_LIST']} not found")
        raise RuntimeError("Invalid Teamwork task list ID")

    response.raise_for_status()
    logging.info(f"Validated Teamwork task list {config['TEAMWORK_TASK_LIST']} exists")

def create_task(title, teamwork_user_id, config):
    url = f"https://{config['TEAMWORK_DOMAIN']}.teamwork.com/tasklists/{config['TEAMWORK_TASK_LIST']}/tasks.json"
    payload = {
        "todo-item": {
            "content": title
        }
    }

    if teamwork_user_id:
        payload["todo-item"]["responsible-party-id"] = teamwork_user_id

    response = requests.post(url, json=payload, headers=get_headers(config))
    response.raise_for_status()
    task_id = response.json()["todo-item"]["id"]
    logging.info(f"Created Teamwork task {task_id} in list {config['TEAMWORK_TASK_LIST']}")
    return task_id

def update_task_status(task_id, completed, config):
    url = f"https://{config['TEAMWORK_DOMAIN']}.teamwork.com/tasks/{task_id}.json"
    data = { "todo-item": { "completed": completed } }
    response = requests.put(url, json=data, headers=get_headers(config))
    response.raise_for_status()

def delete_task(task_id, config):
    url = f"https://{config['TEAMWORK_DOMAIN']}.teamwork.com/tasks/{task_id}.json"
    response = requests.delete(url, headers=get_headers(config))
    response.raise_for_status()

def append_description(task_id, text, config):
    url = f"https://{config['TEAMWORK_DOMAIN']}.teamwork.com/tasks/{task_id}.json"
    # First get the existing task description
    task = requests.get(url, headers=get_headers(config)).json()["todo-item"]
    new_description = (task.get("description") or "") + f"\n{text}"

    data = { "todo-item": { "description": new_description } }
    requests.put(url, json=data, headers=get_headers(config))
