import os
import requests


API_BASE_URL = os.environ.get(
    "API_BASE_URL",
    "http://127.0.0.1:8000/api/demo",
).rstrip("/")


def _handle_response(response):
    if response.status_code == 204:
        return None

    response.raise_for_status()
    return response.json()


# MESSAGE API — ręczny Django CRUD

def get_messages():
    response = requests.get(
        f"{API_BASE_URL}/messages/",
        timeout=5,
    )
    return _handle_response(response)


def create_message(text):
    response = requests.post(
        f"{API_BASE_URL}/messages/",
        json={"text": text},
        timeout=5,
    )
    return _handle_response(response)


def update_message(message_id, text):
    response = requests.put(
        f"{API_BASE_URL}/messages/{message_id}/",
        json={"text": text},
        timeout=5,
    )
    return _handle_response(response)


def delete_message(message_id):
    response = requests.delete(
        f"{API_BASE_URL}/messages/{message_id}/",
        timeout=5,
    )
    return _handle_response(response)


# TASK API — Django REST Framework CRUD

def get_tasks():
    response = requests.get(
        f"{API_BASE_URL}/tasks/",
        timeout=5,
    )
    return _handle_response(response)


def create_task(title, description="", is_done=False):
    response = requests.post(
        f"{API_BASE_URL}/tasks/",
        json={
            "title": title,
            "description": description,
            "is_done": is_done,
        },
        timeout=5,
    )
    return _handle_response(response)


def update_task(task_id, title, description="", is_done=False):
    response = requests.put(
        f"{API_BASE_URL}/tasks/{task_id}/",
        json={
            "title": title,
            "description": description,
            "is_done": is_done,
        },
        timeout=5,
    )
    return _handle_response(response)


def patch_task(task_id, data):
    response = requests.patch(
        f"{API_BASE_URL}/tasks/{task_id}/",
        json=data,
        timeout=5,
    )
    return _handle_response(response)


def delete_task(task_id):
    response = requests.delete(
        f"{API_BASE_URL}/tasks/{task_id}/",
        timeout=5,
    )
    return _handle_response(response)