from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Signal to create a notification when a new message is received.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log old content before a message is updated.
    """
    if instance.pk:  # Message already exists
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        if old_message.content != instance.content:
            # Save old content into history
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content,
                edited_by=old_message.sender  # ensure we track who edited
            )
            instance.edited = True


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal to clean up user-related data when a User is deleted.
    Deletes all messages, notifications, and message histories linked to the user.
    """
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for this user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories linked to messages edited by the user
    MessageHistory.objects.filter(edited_by=instance).delete()
