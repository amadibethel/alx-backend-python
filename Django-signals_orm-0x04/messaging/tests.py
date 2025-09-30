from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, MessageHistory

User = get_user_model()


class MessageEditSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="password123")
        self.receiver = User.objects.create_user(username="bob", password="password123")
        self.message = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Original message"
        )

    def test_message_edit_creates_history(self):
        self.message.content = "Edited message"
        self.message.save()

        history = MessageHistory.objects.filter(message=self.message)
        self.assertTrue(history.exists())
        self.assertEqual(history.first().old_content, "Original message")
        self.assertTrue(self.message.edited)
