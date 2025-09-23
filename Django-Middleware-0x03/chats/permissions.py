from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access.
    - Only participants of a conversation can send, view,
      update (PUT, PATCH), or delete (DELETE) messages.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is part of the conversation
        for all actions (GET, POST, PUT, PATCH, DELETE).
        """
        conversation = getattr(obj, "conversation", None)

        if conversation:
            if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                return request.user in conversation.participants.all()

        return False
