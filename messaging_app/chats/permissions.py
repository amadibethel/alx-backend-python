# chats/permissions.py
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is part of the conversation.
        Assuming Message model has a foreign key 'conversation'
        and Conversation has a ManyToMany field 'participants'.
        """
        conversation = getattr(obj, "conversation", None)
        if conversation:
            return request.user in conversation.participants.all()
        return False
