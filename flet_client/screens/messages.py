import flet as ft
import requests

from api import (
    get_messages,
    create_message,
    delete_message,
)
from navigation import navigation_bar


def messages_view(page: ft.Page):
    input_text = ft.TextField(label="Wpisz wiadomość", autofocus=True)
    status_text = ft.Text()
    messages_column = ft.Column(spacing=8)

    def load_messages():
        messages_column.controls.clear()

        try:
            messages = get_messages()

            if not messages:
                messages_column.controls.append(
                    ft.Text("Brak wiadomości w bazie.")
                )
                return

            for message in messages:
                message_id = message["id"]

                messages_column.controls.append(
                    ft.Row(
                        [
                            ft.Text(
                                f"{message_id}. {message['text']}",
                                expand=True,
                            ),
                            ft.ElevatedButton(
                                "Usuń",
                                on_click=lambda e, message_id=message_id: remove_message(message_id),
                            ),
                        ]
                    )
                )

        except requests.RequestException as error:
            messages_column.controls.append(
                ft.Text(f"Błąd pobierania wiadomości: {error}")
            )

    def send_message(e):
        text = input_text.value.strip()

        if not text:
            status_text.value = "Wpisz tekst."
            page.update()
            return

        try:
            create_message(text)

            input_text.value = ""
            status_text.value = "Dodano wiadomość."
            load_messages()

        except requests.RequestException as error:
            status_text.value = f"Błąd zapisu: {error}"

        page.update()

    def remove_message(message_id):
        try:
            delete_message(message_id)

            status_text.value = f"Usunięto wiadomość ID {message_id}."
            load_messages()

        except requests.RequestException as error:
            status_text.value = f"Błąd usuwania: {error}"

        page.update()

    def refresh(e):
        load_messages()
        status_text.value = "Odświeżono."
        page.update()

    load_messages()

    return ft.View(
        route="/messages",
        controls=[
            ft.AppBar(title=ft.Text("Messages CRUD")),
            navigation_bar(page),

            ft.Text("Messages — ręczne Django API", size=24),

            input_text,
            ft.Row(
                [
                    ft.ElevatedButton("Wyślij", on_click=send_message),
                    ft.ElevatedButton("Odśwież", on_click=refresh),
                ]
            ),

            status_text,
            ft.Divider(),
            messages_column,
        ],
        scroll=ft.ScrollMode.AUTO,
    )