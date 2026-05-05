from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

rounter = DefaultRouter()
rounter.register("tesk", views.TaskViewSet, basename="task")

urlpatterns = [
    path("ping/", views.ping, name="demo-ping"),
    path("messages/", views.messages, name="demo-messages"),
    path("messages/<int:message_id>/", views.message_details, name="delete-message"),
    path("", include(rounter.urls)),
]

