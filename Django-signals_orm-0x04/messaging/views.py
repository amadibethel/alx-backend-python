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
    Delete the logged-in user's account.
    Triggers post_delete signal for cleanup.
    """
    user = request.user
    username = user.username
    user.delete()
    messages.success(request, f"Account '{username}' deleted successfully.")
    return redirect("home")


@login_required
def send_message(request, receiver_id):
    """
    Send a new message (optionally as a reply to parent message).
    """
    if request.method == "POST":
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")

        parent_message = None
        if parent_id:
            parent_message = get_object_or_404(Message, id=parent_id)

        message = Message.objects.create(
            sender=request.user,
            receiver_id=receiver_id,
            content=content,
            parent_message=parent_message
        )
        return JsonResponse({"message": "Message sent", "id": message.id})


def build_thread(message):
    """
    Recursive helper to fetch replies for a message using filter().
    Optimized with select_related + prefetch_related.
    """
    replies_qs = (
        Message.objects.filter(parent_message=message)
        .select_related("sender", "receiver")
        .prefetch_related("replies")
        .order_by("timestamp")
    )

    thread = []
    for reply in replies_qs:
        thread.append({
            "id": reply.id,
            "sender": reply.sender.username,
            "receiver": reply.receiver.username,
            "content": reply.content,
            "timestamp": reply.timestamp,
            "replies": build_thread(reply)
        })
    return thread


@login_required
def conversation_thread(request, message_id):
    """
    Fetch all replies for a message in threaded format.
    """
    message = get_object_or_404(
        Message.objects.select_related("sender", "receiver"), id=message_id
    )

    data = {
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "replies": build_thread(message)
    }
    return JsonResponse(data)


@login_required
def inbox(request):
    """
    Display all unread messages for the logged-in user.
    Uses custom manager 'unread' with optimized .only() query.
    """
    unread_messages = Message.unread.unread_for_user(request.user)

    messages_data = [
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
        for msg in unread_messages
    ]

    return JsonResponse({"unread_messages": messages_data})
