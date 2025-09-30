from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()


class MessagingSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="password123")
        self.receiver = User.objects.create_user(username="bob", password="password123")

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello Bob!"
        )

        notification = Notification.objects.filter(user=self.receiver, message=message)
        self.assertTrue(notification.exists())
        self.assertEqual(notification.count(), 1)
