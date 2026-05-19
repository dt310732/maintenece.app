import flet as ft


def navigation_bar(page: ft.Page):
    return ft.Row(
        [
            ft.ElevatedButton(
                "Messages",
                on_click=lambda e: page.go("/messages"),
            ),
            ft.ElevatedButton(
                "Tasks",
                on_click=lambda e: page.go("/tasks"),
            ),
        ],
        spacing=10,
    )