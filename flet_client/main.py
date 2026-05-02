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
                    ft.Row(
                        [
                            ft.Text(
                                f"{message['id']}. {message['text']} "
                                f"({message['created_at']})",
                                expand=True
                            ),
                            ft.ElevatedButton(
                                "Usuń",
                                on_click= lambda e, message_id = message['id']: delete_message(message_id),
                            ),
                        ]
                    )
                )
        except requests.RequestException as error:
            messages_column.controls.append(
                ft.Text(f"Błąd pobierania danych: {error}")
            )
    
    def refresh_messages(e):
        load_messages()
        status_text.value = "Odświeżono liste"
        page.update()

    def clear_input(e):
        input_text.value = ""
        page.update()

    def send_message(e):
        text = input_text.value.strip()

        if not text:
            status_text.value = "Wpisz tekst przed wyslaniem"
            page.update()
            return
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/messages/",
                json={'text': text},
                timeout=5,
            )
            response.raise_for_status()

            input_text.value = ""
            status_text.value = "Zapisano w Django/Postgres."

            load_messages()
        except requests.RequestException as error:
            status_text.value = f'Błąd zapisu: {error}'
        
        page.update()


    def delete_message(message_id: int) -> None:
        try:
            response = requests.delete(
                f"{API_BASE_URL}/messages/{message_id}/",
                timeout=5
            )
            response.raise_for_status()

            status_text.value = f"Usunięto wiadomość ID {message_id}"
            load_messages()
        except requests.RequestException as error:
            status_text.value = f"Bląd usuwania {error}"
        page.update()

    page.add(
        ft.Text("Flet → Django API → PostgreSQL", size=24),
        input_text,
        ft.Row(
            [
                ft.ElevatedButton("Wyślij", on_click=send_message),
                ft.ElevatedButton("Odśwież", on_click=refresh_messages),
                ft.ElevatedButton("Wyczyść", on_click=clear_input),
            ]
        ),
        status_text,
        ft.Divider(),
        ft.Text("Wiadomości z bazy:", size=18),
        messages_column,
    )  
    
    load_messages()
    page.update()

ft.app(target=main)