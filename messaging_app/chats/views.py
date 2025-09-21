from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for handling conversations."""
    
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["participants__first_name", "participants__last_name", "participants__email"]

    def get_queryset(self):
        # Only show conversations where the user is a participant
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
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
        conversation = get_object_or_404(Conversation, pk=pk)

        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant of this conversation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = Message.objects.create(
            conversation=conversation,
            sender_id=request.data.get("sender"),
            message_body=request.data.get("message_body"),
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet
