import requests
import logging

def get_headers(config):
    return {
        "Authorization": f"Bearer {config['TEAMWORK_API_TOKEN']}",
        "Content-Type": "application/json"
    }

def create_task(title, teamwork_user_id, config):
    url = f"https://{config['TEAMWORK_DOMAIN']}.teamwork.com/projects/{config['TEAMWORK_PROJECT_ID']}/tasks.json"
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
    logging.info(f"Created Teamwork task {task_id}")
    return task_id

def update_task_status(task_id, completed, config):
    url = f"https://{config['TEAMWORK_DOMAIN']}.teamwork.com/tasks/{task_id}.json"
    payload = {
        "todo-item": {
            "completed": completed
        }
    }
    response = requests.put(url, json=payload, headers=get_headers(config))
    response.raise_for_status()
    logging.info(f"Marked task {task_id} as {'complete' if completed else 'incomplete'}")

def delete_task(task_id, config):
    url = f"https://{config['TEAMWORK_DOMAIN']}.teamwork.com/tasks/{task_id}.json"
    response = requests.delete(url, headers=get_headers(config))
    response.raise_for_status()
    logging.info(f"Deleted task {task_id}")
