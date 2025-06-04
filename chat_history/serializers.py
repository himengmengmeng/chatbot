from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.core.validators import MinValueValidator
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['role', 'content', 'timestamp']
        read_only_fields = ['timestamp']

class MessageAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']        

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at']

class ConversationAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = []  # 用户从请求中自动关联






