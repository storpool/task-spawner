import requests

def get_headers(config):
    return {
        "Authorization": f"Bearer {config['TEAMWORK_API_TOKEN']}",
        "Content-Type": "application/json"
    }

def create_task(subject, ticket_number, teamwork_user_id, config):
    url = f"https://{config['TEAMWORK_DOMAIN']}.teamwork.com/tasks.json"
    task_name = f"[Ticket #{ticket_number}] {subject}"

    data = {
        "todo-item": {
            "content": task_name,
            "tasklist-id": config["TEAMWORK_TASK_LIST_ID"],
        }
    }

    if teamwork_user_id:
        data["todo-item"]["responsible-party-id"] = teamwork_user_id

    response = requests.post(url, json=data, headers=get_headers(config))
    response.raise_for_status()
    return response.json()["todo-item"]["id"]

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
