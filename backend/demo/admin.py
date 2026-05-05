from django.contrib import admin
from .models import Message, Task

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin): # type: ignore
    list_display = ("id", "text", "created_at")
    search_fields = ("text",)

@admin.register(Task)
class TaskAdmin(Task):
    list_display = ("id", "title", "is_done", "created_at")
    search_fields = ("title", "description")
    list_filter = ("is_done",)