# Django 核心
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Django REST framework 核心
from rest_framework import (
    status,
    mixins,
    generics,
    viewsets,
    permissions,
    filters,
    pagination,
    exceptions,
    decorators
)
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import PageNumberPagination

# 过滤相关
import django_filters
from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet
)

# 项目特定模块
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationAddSerializer,
    MessageAddSerializer
)

# 第三方库
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class ConversationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conversation.objects.select_related('user').all()  # 性能优化关键点
    
    def get_serializer_class(self):
        return ConversationAddSerializer if self.action == 'create' else ConversationSerializer

    def get_queryset(self):
        """ 仅返回当前用户的会话（已优化关联查询） """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """ 创建会话时自动关联当前用户 """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """ 
        请求体示例:
        {"message": "你好，请介绍一下你自己"}
        
        """
        try:
            conversation = self.get_object()
            user_message = request.data.get('message')
            
            # 保存用户消息
            conversation.messages.create(
                role='human',
                content=user_message
            )
            
            # 调用GPT-4o生成回复
            model = ChatOpenAI(model="gpt-4o")
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in conversation.messages.all()
            ]
            result = model.invoke(history + [{"role": "user", "content": user_message}])
            
            # 保存AI回复
            conversation.messages.create(
                role='ai',
                content=result.content
            )
            
            return Response({'response': result.content})
            
        except Exception as e:
            return Response(
                {"error": "AI服务暂时不可用，请稍后重试"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class MessageViewSet(ModelViewSet):
    serializer_class = MessageAddSerializer
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()  # 关键修复
    
    def get_queryset(self):
        return self.queryset.filter(conversation__user=self.request.user)
    













