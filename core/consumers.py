from channels.generic.websocket import AsyncWebsocketConsumer
import json


class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_group_name = "rooms"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        print("WebSocket Connected")

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print("WebSocket Disconnected")

    async def receive(self, text_data):

        pass

    async def room_update(self, event):

        await self.send(text_data=json.dumps({

    "type": event["type"],

    "room_type": event["room_type"],

    "room_id": event["room_id"],

    "status": event["status"],

    "occupied_beds": event["occupied_beds"],

    "capacity": event["capacity"],

    "remaining_beds": event["remaining_beds"],

    "progress": event["progress"]

}))