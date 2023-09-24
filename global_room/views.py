from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message


@login_required
def global_room(request):
    data = {
        "msg_data": Message.objects.all()
    }
    return render(request, "global_room/chat_room.html", data)