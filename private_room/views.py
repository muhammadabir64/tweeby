from django.shortcuts import render
from django.db.models import Q
from account.models import Account
from .models import Message


def messages(request):
    data = {
        "users_list": Account.objects.get(user=request.user).following.all()
    }
    return render(request, "private_room/messages.html", data)


def chat_room(request, thread_self, thread):
    user_data = Account.objects.get(thread_code=thread)
    users_list = Account.objects.get(user=request.user).following.all()
    message_data = Message.objects.filter(
            Q(room=f"{thread_self}u{thread}") | 
            Q(room=f"{thread}u{thread_self}")).all()

    data = {
        "user_data": user_data,
        "users_list": users_list,
        "message_data": message_data
    }
    return render(request, "private_room/chat_room.html", data)