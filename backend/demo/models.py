from django.db import models

class Message(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text
    
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    