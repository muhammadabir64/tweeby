from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from django.db.models import Q
from account.models import Account
from .models import Message


class PrivateRoomConsumer(JsonWebsocketConsumer):
    def connect(self):
        thread_self = self.scope["url_route"]["kwargs"]["thread_self"]
        thread = self.scope["url_route"]["kwargs"]["thread"]
        user_self = Account.objects.get(thread_code=thread_self)
        user = Account.objects.get(thread_code=thread)

        if user_self.id > user.id:
            self.room_group_name = f"{thread_self}u{thread}"
        else:
            self.room_group_name = f"{thread}u{thread_self}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
    
    def receive_json(self, content, **kwargs):
        user = Account.objects.get(user__username=content["username"])
        msg = Message(user=user, text=content["message"], room=self.room_group_name)
        msg.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "room_message",
                "message": msg.text,
                "username": msg.user.user.username,
                "avatar": msg.user.profile_img,
                "timestamp": str(msg.timestamp.strftime("%b %d %Y, %I:%M %p"))
            }
        )
    

    def room_message(self, data):
        self.send_json(data)