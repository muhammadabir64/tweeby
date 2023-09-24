from django.urls import path
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tweeby.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from private_room.consumers import PrivateRoomConsumer
from global_room.consumers import GlobalRoomConsumer

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/global_room/", GlobalRoomConsumer.as_asgi()),
            path("ws/<str:thread_self>u<str:thread>/", PrivateRoomConsumer.as_asgi())
        ])
    )
})