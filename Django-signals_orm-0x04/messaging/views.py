from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from .models import Message

User = get_user_model()


@login_required
def delete_user(request):
    """
    View to allow a user to delete their account.
    """
    user = request.user
    username = user.username
    user.delete()  # This triggers post_delete signal

    messages.success(request, f"Account '{username}' deleted successfully.")
    return redirect("home")  # redirect to home or login page


@login_required
def send_message(request, receiver_id):
    """
    View to send a new message.
    """
    if request.method == "POST":
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")

        parent_message = None
        if parent_id:
            parent_message = get_object_or_404(Message, id=parent_id)

        message = Message.objects.create(
            sender=request.user,               # required in tests
            receiver_id=receiver_id,           # required in tests
            content=content,
            parent_message=parent_message
        )
        return JsonResponse({"message": "Message sent", "id": message.id})


@login_required
def conversation_thread(request, message_id):
    """
    Recursive query to fetch all replies for a given message in threaded format.
    Optimized with select_related + prefetch_related.
    """
    message = (
        Message.objects
        .select_related("sender", "receiver")
        .prefetch_related("replies")
        .get(id=message_id)
    )

    data = {
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "replies": message.get_thread()  # recursion happens in model
    }
    return JsonResponse(data)
