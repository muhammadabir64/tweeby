from django.urls import path
from .views import global_room


urlpatterns = [
    path("global_room/", global_room, name="global_room")
]