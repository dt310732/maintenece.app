from django.urls import path
from . import views

urlpatterns = [
    path("ping/", views.ping, name="demo-ping"),
    path("messages/", views.messages, name="demo-messages"),
    path("message/<int:message_id>/", views.message_details, name="delete-message")
]