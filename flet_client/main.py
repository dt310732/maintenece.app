import flet as ft


def main(page: ft.Page):
    page.title = "CMMS Dev"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Column(
            controls=[
                ft.Text("CMMS Dev działa", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Flet client uruchomiony w Dockerze"),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


ft.app(target=main, view=ft.WEB_BROWSER)