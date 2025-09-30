from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)  # track read/unread
    edited_by = models.ForeignKey(
        User, null=True, blank=True, related_name="edited_messages", on_delete=models.SET_NULL
    )
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    # Managers
    objects = models.Manager()        # default
    unread = UnreadMessagesManager()  # custom manager

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}: {self.content[:20]}"

    def get_thread(self):
        """
        Recursive method to fetch all replies to this message.
        Optimized with select_related and prefetch_related.
        """
        replies = (
            Message.objects.filter(parent_message=self)
            .select_related("sender", "receiver")
            .prefetch_related("replies")
            .order_by("timestamp")
        )
        thread = []
        for reply in replies:
            thread.append({
                "id": reply.id,
                "sender": reply.sender.username,
                "receiver": reply.receiver.username,
                "content": reply.content,
                "timestamp": reply.timestamp,
                "replies": reply.get_thread()  # recursive call
            })
        return thread


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, related_name="history", on_delete=models.CASCADE
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User, null=True, blank=True, related_name="message_edits", on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"History of Message {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    user = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        Message, related_name="notifications", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} - Message {self.message.id}"
