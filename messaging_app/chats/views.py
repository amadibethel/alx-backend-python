# messaging_app/chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for handling conversations."""

    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects a list of participant user_ids.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation = Conversation.objects.create()
        participants = request.data.get("participants", [])
        if participants:
            conversation.participants.set(participants)

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        """
        Send a new message to an existing conversation.
        Expects: { "sender": <user_id>, "message_body": "..." }
        """
        conversation = get_object_or_404(Conversation, pk=pk)
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = Message.objects.create(
            conversation=conversation,
            sender_id=request.data.get("sender"),
            message_body=request.data.get("message_body"),
        )
        return Response(
            MessageSerializer(message).data, status=status.HTTP_201_CREATED
        )


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for handling messages."""

    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer
