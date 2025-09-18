# messaging_app/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("chats.urls")),  # expose chats app under /api/
]
