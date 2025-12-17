import json

from channels.generic.websocket import AsyncWebsocketConsumer


class CreditoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "credito"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def credito_change(self, event):
        await self.send(text_data=json.dumps({"message": event["payload"]}))

    async def credito_delete(self, event):
        await self.send(text_data=json.dumps({"message": event["payload"]}))
