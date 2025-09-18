# messaging_app/chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message


# ------------------------
# User Serializer
# ------------------------
class UserSerializer(serializers.ModelSerializer):
    # Explicit CharField usage
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
            "full_name",
        ]


# ------------------------
# Message Serializer
# ------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
        ]


# ------------------------
# Conversation Serializer
# ------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    # Explicit SerializerMethodField usage
    participant_count = serializers.SerializerMethodField()

    def get_participant_count(self, obj):
        return obj.participants.count()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "participant_count",
            "created_at",
        ]

    # Example of custom validation with ValidationError
    def validate(self, data):
        if "participants" in data and len(data["participants"]) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least 2 participants."
            )
        return data
