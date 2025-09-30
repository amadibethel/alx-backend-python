from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

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
