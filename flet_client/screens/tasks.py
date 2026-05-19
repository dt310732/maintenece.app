import flet as ft
import requests

from api import (
    get_tasks,
    create_task,
    update_task,
    patch_task,
    delete_task,
)
from navigation import navigation_bar


def tasks_view(page: ft.Page):
    status_text = ft.Text()

    title_input = ft.TextField(label="Tytuł")
    description_input = ft.TextField(label="Opis")
    is_done_checkbox = ft.Checkbox(label="Wykonane")

    edit_id_input = ft.TextField(label="ID do edycji", width=150)
    edit_title_input = ft.TextField(label="Nowy tytuł")
    edit_description_input = ft.TextField(label="Nowy opis")
    edit_is_done_checkbox = ft.Checkbox(label="Wykonane")

    tasks_column = ft.Column(spacing=8)

    def load_tasks():
        tasks_column.controls.clear()

        try:
            tasks = get_tasks()

            if not tasks:
                tasks_column.controls.append(
                    ft.Text("Brak tasków w bazie.")
                )
                return

            for task in tasks:
                task_id = task["id"]
                title = task["title"]
                description = task["description"]
                is_done = task["is_done"]

                tasks_column.controls.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(
                                            f"ID {task_id}: {title}",
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(description or "Brak opisu"),
                                        ft.Text(
                                            "Status: wykonane"
                                            if is_done
                                            else "Status: niewykonane"
                                        ),
                                    ],
                                    expand=True,
                                ),
                                ft.ElevatedButton(
                                    "Toggle",
                                    on_click=lambda e, task_id=task_id, is_done=is_done: toggle_task(task_id, is_done),
                                ),
                                ft.ElevatedButton(
                                    "Usuń",
                                    on_click=lambda e, task_id=task_id: remove_task(task_id),
                                ),
                            ]
                        ),
                        border=ft.border.all(1),
                        padding=10,
                        border_radius=8,
                    )
                )

        except requests.RequestException as error:
            tasks_column.controls.append(
                ft.Text(f"Błąd pobierania tasków: {error}")
            )

    def add_task(e):
        title = title_input.value.strip()
        description = description_input.value.strip()
        is_done = is_done_checkbox.value

        if not title:
            status_text.value = "Tytuł jest wymagany."
            page.update()
            return

        try:
            create_task(
                title=title,
                description=description,
                is_done=is_done,
            )

            title_input.value = ""
            description_input.value = ""
            is_done_checkbox.value = False

            status_text.value = "Dodano task."
            load_tasks()

        except requests.RequestException as error:
            status_text.value = f"Błąd dodawania taska: {error}"

        page.update()

    def edit_task(e):
        task_id = edit_id_input.value.strip()
        title = edit_title_input.value.strip()
        description = edit_description_input.value.strip()
        is_done = edit_is_done_checkbox.value

        if not task_id.isdigit():
            status_text.value = "ID musi być liczbą."
            page.update()
            return

        if not title:
            status_text.value = "Tytuł jest wymagany przy PUT."
            page.update()
            return

        try:
            update_task(
                task_id=task_id,
                title=title,
                description=description,
                is_done=is_done,
            )

            edit_id_input.value = ""
            edit_title_input.value = ""
            edit_description_input.value = ""
            edit_is_done_checkbox.value = False

            status_text.value = f"Zaktualizowano task ID {task_id}."
            load_tasks()

        except requests.RequestException as error:
            status_text.value = f"Błąd aktualizacji taska: {error}"

        page.update()

    def toggle_task(task_id, current_is_done):
        try:
            patch_task(
                task_id=task_id,
                data={"is_done": not current_is_done},
            )

            status_text.value = f"Zmieniono status taska ID {task_id}."
            load_tasks()

        except requests.RequestException as error:
            status_text.value = f"Błąd PATCH: {error}"

        page.update()

    def remove_task(task_id):
        try:
            delete_task(task_id)

            status_text.value = f"Usunięto task ID {task_id}."
            load_tasks()

        except requests.RequestException as error:
            status_text.value = f"Błąd usuwania taska: {error}"

        page.update()

    def refresh(e):
        load_tasks()
        status_text.value = "Odświeżono."
        page.update()

    load_tasks()

    return ft.View(
        route="/tasks",
        controls=[
            ft.AppBar(title=ft.Text("Tasks CRUD")),
            navigation_bar(page),

            ft.Text("Tasks — Django REST Framework", size=24),

            ft.Divider(),

            ft.Text("CREATE", size=18),
            title_input,
            description_input,
            is_done_checkbox,
            ft.ElevatedButton("Dodaj task", on_click=add_task),

            ft.Divider(),

            ft.Text("UPDATE PUT", size=18),
            edit_id_input,
            edit_title_input,
            edit_description_input,
            edit_is_done_checkbox,
            ft.ElevatedButton("Zaktualizuj task", on_click=edit_task),

            ft.Divider(),

            ft.Row(
                [
                    ft.Text("Lista tasków", size=18),
                    ft.ElevatedButton("Odśwież", on_click=refresh),
                ]
            ),

            status_text,
            tasks_column,
        ],
        scroll=ft.ScrollMode.AUTO,
    )