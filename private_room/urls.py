from django.urls import path
from .views import messages, chat_room


urlpatterns = [
    path("messages/", messages, name="messages"),
    path("messages/<str:thread_self>u<str:thread>/", chat_room, name="chat_room")
]