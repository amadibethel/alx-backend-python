# messaging_app/chats/urls.py

from django.urls import path, include
from rest_framework import routers   # explicit import
from .views import ConversationViewSet, MessageViewSet

# Use routers.DefaultRouter()
router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
]
