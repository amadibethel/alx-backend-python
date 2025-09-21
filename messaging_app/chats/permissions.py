# messaging_app/chats/permissions.py
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission: only allow users to access their own messages/conversations
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
