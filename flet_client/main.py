import flet as ft
import os 
import requests

API_BASE_URL = os.environ.get(
    "API_BASE_URL",
).rstrip("/")

def main(page: ft.Page):
    page.title = "Django + Flet Demo"
    page.window.height = 600
    page.window.width = 700

    input_text = ft.TextField(
        label="Wpisz wiadomość",
        autofocus=True,
    )

    status_text = ft.Text("")
    messages_column = ft.Column(spacing=8)

    def load_messages():
        messages_column.controls.clear()

        try:
            response = requests.get(
                f"{API_BASE_URL}/messages/",
                timeout=5
            )
            response.raise_for_status()

            messages = response.json()

            if not messages:
                messages_column.controls.append(
                    ft.Text("Brak wiadomości w bazie.")
                )
                return
            
            for message in messages:
                messages_column.controls.append(
                    ft.Text(
                        f"{message['id']}. {message['text']}"
                        f"({message['created_at']})"
                    )
                )
        except requests.RequestException as error:
            messages_column.controls.append(
                ft.Text(f"Błąd pobierania danych: {error}")
            )
    page.add(
        ft.Text("Django + Flet Demo", size=24, weight=ft.FontWeight.BOLD),
        input_text,
        status_text,
        messages_column,
    )  
    load_messages()
    page.update()


ft.app(target=main, view=ft.WEB_BROWSER)