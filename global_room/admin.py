from django.contrib import admin
from django.template.defaultfilters import truncatechars
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "sender", "message", "time"]
    list_display_links = ["id", "sender", "message", "time"]
    list_per_page = 25

    def message(self, obj):
        return truncatechars(obj.text, 25)

    def time(self, obj):
        return obj.timestamp.strftime("%d %b %Y | %H:%M:%S")