from django.contrib import admin
from .models import Message, Notification, MessageHistory


class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ("old_content", "edited_at")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "content", "timestamp", "edited")
    inlines = [MessageHistoryInline]
    search_fields = ("sender__username", "receiver__username", "content")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("user__username", "message__content")


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "old_content", "edited_at")
    readonly_fields = ("message", "old_content", "edited_at")
