import flet as ft

from screens.messages import messages_view
from screens.tasks import tasks_view


def main(page: ft.Page):
    page.title = "Flet + Django Learning"

    def route_change(e):
        page.views.clear()

        if page.route == "/tasks":
            page.views.append(tasks_view(page))
        else:
            page.views.append(messages_view(page))

        page.update()

    def view_pop(e):
        page.views.pop()

        if page.views:
            page.go(page.views[-1].route)
        else:
            page.go("/messages")

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route or "/messages")


ft.app(target=main)