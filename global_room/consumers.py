from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message


class GlobalRoomConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_group_name = "global_room"
        self.user = self.scope["user"]

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "room_join_msg",
                "username": self.user.username,
                "avatar": self.user.account.profile_img
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "room_left_msg",
                "username": self.user.username,
                "avatar": self.user.account.profile_img
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
    
    def receive_json(self, content, **kwargs):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "room_message",
                "msg_data": content
            }
        )
    

    def room_message(self, data):
        msg = Message(sender=self.user.account, text=data["msg_data"]["message"])
        msg.save()
        data["msg_data"]["timestamp"] = str(msg.timestamp.strftime("%b %d %Y, %I:%M %p"))
        self.send_json(data)
    

    def room_join_msg(self, data):
        data["total_users"] = len(self.channel_layer.groups.get(self.room_group_name, {}).items())
        self.send_json(data)
        
    def room_left_msg(self, data):
        data["total_users"] = len(self.channel_layer.groups.get(self.room_group_name, {}).items())
        self.send_json(data)