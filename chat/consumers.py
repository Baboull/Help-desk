import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from tickets.models import Ticket

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.room_group_name = f'chat_{self.ticket_id}'
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
            return

        can_access = await self.can_access_ticket(self.ticket_id, self.user)
        if not can_access:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json.get('message', '').strip()

        if not message_content:
            return
            
        is_open = await self.is_ticket_open(self.ticket_id)
        if not is_open:
            await self.send(text_data=json.dumps({
                'error': 'Cannot send messages on a resolved or closed ticket.'
            }))
            return

        msg_obj = await self.save_message(self.ticket_id, self.user, message_content)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg_obj.content,
                'sender_id': self.user.id,
                'sender_username': self.user.username,
                'time': msg_obj.created_at.strftime('%H:%M')
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'time': event['time']
        }))

    @database_sync_to_async
    def can_access_ticket(self, ticket_id, user):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if user.role in ['staff', 'admin'] or user.is_staff:
                return True
            return ticket.client == user
        except Ticket.DoesNotExist:
            return False

    @database_sync_to_async
    def is_ticket_open(self, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            return ticket.status not in ['resolved', 'closed']
        except Ticket.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, ticket_id, user, content):
        ticket = Ticket.objects.get(id=ticket_id)
        return Message.objects.create(ticket=ticket, sender=user, content=content)
