from django.db import models
from user.models import User



class InAppChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_chats")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver_chats")
    message = models.TextField(blank=True, verbose_name="Chat contents")
    is_read = models.BooleanField(default=False)
    unique_identifier = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return f"{self.sender} --> {self.receiver}"

    class Meta:
        ordering = ["-created_at"]
