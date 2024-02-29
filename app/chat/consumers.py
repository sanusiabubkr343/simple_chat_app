from channels.generic.websocket import AsyncWebsocketConsumer

import json
import time

from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        #decided to move all synchronous import here due to app registry exception
       
        from rest_framework_simplejwt.tokens import UntypedToken
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import AnonymousUser

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        try:
            token = self.scope['query_string'].decode('utf-8').split('token=')[1]

            decoded_data = UntypedToken(token).payload
            user_id = decoded_data['user_id']

            user = await database_sync_to_async(get_user_model().objects.get)(pk=user_id)
        except (InvalidToken,IndexError, TokenError, get_user_model().DoesNotExist):
            user = AnonymousUser()

        if isinstance(user, AnonymousUser):

            # decided to accept the socket so as to send the error message before closing it
            await self.accept()

            await self.send(text_data=json.dumps({"error": "Authentication invalid or not provided"}))

            await self.close()
        else:

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            self.scope['user'] = user

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        # inline importing to avoid circular dependency during deployment
        from chat.models import InAppChat
        from user.models import User

        if text_data:
            try:
                text_data_json = json.loads(text_data)
                message = text_data_json.get("message")
                receiver = text_data_json.get("receiver")
                unique_identifier = text_data_json.get("unique_identifier")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON format: {e}")
                return

            receiver = await database_sync_to_async(User.objects.get)(pk=receiver)
            created_at = int(time.time())  # time stamp to be used in real time

            chat_message = InAppChat(
                sender=self.scope['user'],
                receiver=receiver,
                message=message,
                unique_identifier=unique_identifier,
            )
            await database_sync_to_async(chat_message.save)()

            # Proceed with sending message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    "message": message,
                    "sender": self.scope['user'].pk,
                    "receiver": receiver.pk,
                    "unique_identifier": unique_identifier,
                    "created_at": created_at,
                },
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        receiver = event["receiver"]
        unique_identifier = event["unique_identifier"]
        created_at = event["created_at"]

        # Send the received message back to the client
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": self.scope['user'].pk,
                    "receiver": receiver,
                    "unique_identifier": unique_identifier,
                    "created_at": created_at,
                }
            )
        )
