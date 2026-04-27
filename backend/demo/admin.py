from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin): # type: ignore
    list_display = ("id", "text", "created_at")
    search_fields = ("text",)

