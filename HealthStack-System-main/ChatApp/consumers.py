"""
WebSocket Consumer for Real-time Chat
Handles WebSocket connections for doctor-patient messaging
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import chatMessages

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time chat between doctors and patients
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.room_name = f"chat_{self.user.id}"
        self.room_group_name = f"chat_group_{self.user.id}"
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send online status
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to chat server',
            'user_id': self.user.id
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """
        Receive message from WebSocket
        Handle different message types: chat_message, typing, read_receipt
        """
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'chat_message')
            
            if message_type == 'chat_message':
                await self.handle_chat_message(data)
            elif message_type == 'typing':
                await self.handle_typing(data)
            elif message_type == 'read_receipt':
                await self.handle_read_receipt(data)
            elif message_type == 'get_messages':
                await self.handle_get_messages(data)
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))
    
    async def handle_chat_message(self, data):
        """Handle incoming chat message"""
        message_text = data.get('message', '').strip()
        recipient_id = data.get('recipient_id')
        
        if not message_text or not recipient_id:
            return
        
        # Save message to database
        message_obj = await self.save_message(
            user_from_id=self.user.id,
            user_to_id=recipient_id,
            message=message_text
        )
        
        if message_obj:
            # Send message to recipient's group
            recipient_group = f"chat_group_{recipient_id}"
            await self.channel_layer.group_send(
                recipient_group,
                {
                    'type': 'chat_message_handler',
                    'message': {
                        'id': message_obj.id,
                        'user_from': self.user.id,
                        'user_to': recipient_id,
                        'message': message_text,
                        'date_created': message_obj.date_created.strftime("%b-%d-%Y %H:%M"),
                        'sender_name': f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
                    }
                }
            )
            
            # Send confirmation to sender
            await self.send(text_data=json.dumps({
                'type': 'message_sent',
                'message': {
                    'id': message_obj.id,
                    'user_from': self.user.id,
                    'user_to': recipient_id,
                    'message': message_text,
                    'date_created': message_obj.date_created.strftime("%b-%d-%Y %H:%M")
                }
            }))
    
    async def handle_typing(self, data):
        """Handle typing indicator"""
        recipient_id = data.get('recipient_id')
        is_typing = data.get('is_typing', False)
        
        if recipient_id:
            recipient_group = f"chat_group_{recipient_id}"
            await self.channel_layer.group_send(
                recipient_group,
                {
                    'type': 'typing_indicator',
                    'user_id': self.user.id,
                    'is_typing': is_typing,
                    'user_name': f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
                }
            )
    
    async def handle_read_receipt(self, data):
        """Handle message read receipt"""
        message_id = data.get('message_id')
        sender_id = data.get('sender_id')
        
        if sender_id:
            sender_group = f"chat_group_{sender_id}"
            await self.channel_layer.group_send(
                sender_group,
                {
                    'type': 'read_receipt_handler',
                    'message_id': message_id,
                    'read_by': self.user.id
                }
            )
    
    async def handle_get_messages(self, data):
        """Fetch chat history"""
        other_user_id = data.get('other_user_id')
        last_id = data.get('last_id', 0)
        
        if other_user_id:
            messages = await self.get_chat_messages(
                user1_id=self.user.id,
                user2_id=other_user_id,
                last_id=last_id
            )
            
            await self.send(text_data=json.dumps({
                'type': 'message_history',
                'messages': messages
            }))
    
    # Handlers for group messages
    async def chat_message_handler(self, event):
        """Send chat message to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': event['message']
        }))
    
    async def typing_indicator(self, event):
        """Send typing indicator to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user_id': event['user_id'],
            'is_typing': event['is_typing'],
            'user_name': event['user_name']
        }))
    
    async def read_receipt_handler(self, event):
        """Send read receipt to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'message_id': event['message_id'],
            'read_by': event['read_by']
        }))
    
    # Database operations
    @database_sync_to_async
    def save_message(self, user_from_id, user_to_id, message):
        """Save message to database"""
        try:
            user_from = User.objects.get(id=user_from_id)
            user_to = User.objects.get(id=user_to_id)
            
            msg = chatMessages.objects.create(
                user_from=user_from,
                user_to=user_to,
                message=message
            )
            return msg
        except Exception as e:
            print(f"Error saving message: {e}")
            return None
    
    @database_sync_to_async
    def get_chat_messages(self, user1_id, user2_id, last_id=0):
        """Get chat messages between two users"""
        try:
            messages = chatMessages.objects.filter(
                id__gt=last_id
            ).filter(
                models.Q(user_from_id=user1_id, user_to_id=user2_id) |
                models.Q(user_from_id=user2_id, user_to_id=user1_id)
            ).order_by('date_created')[:50]  # Limit to last 50 messages
            
            return [
                {
                    'id': msg.id,
                    'user_from': msg.user_from.id,
                    'user_to': msg.user_to.id,
                    'message': msg.message,
                    'date_created': msg.date_created.strftime("%b-%d-%Y %H:%M")
                }
                for msg in messages
            ]
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return []


# Import models for queries
from django.db import models
