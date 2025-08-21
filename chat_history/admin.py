from functools import partial, partialmethod
from typing import Any
from unittest import case
from django.db.models import Count, Sum, Case, When, IntegerField
from django.contrib import admin
from django.db.models.query import QuerySet
from django.forms import IntegerField
from django.http.request import HttpRequest
from . import models
from django.db.models.aggregates import Count, Max, Min, Sum
from django.db.models import F
from django.utils.html import format_html
from urllib.parse import urlencode
from django.urls import reverse
from django.db.models.functions import Concat
from django.db.models.fields import CharField
from django.db.models import F, Count, Sum, Value
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Concat
from django.contrib import admin
from django.utils.html import format_html
from .models import Conversation, Message
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# 添加发送消息的表单
class MessageForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 80}),
        label='发送消息'
    )

# 内联显示 Message（在 Conversation 详情页）
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ('role', 'content', 'timestamp')
    readonly_fields = ('timestamp',)
    can_delete = False  # 禁用删除选项

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'linked_user', 'created_at')
    list_display_links = ('id',)
    inlines = [MessageInline]
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'id')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)
    
    # 添加自定义视图
    change_form_template = 'admin/chat_history/conversation/change_form.html'
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/send_message/',
                 self.admin_site.admin_view(self.send_message),
                 name='chat_history_conversation_send_message'),
        ]
        return custom_urls + urls
    
    def send_message(self, request, object_id):
        if request.method != 'POST':
            return HttpResponseRedirect('..')
        
        conversation = self.get_object(request, object_id)
        form = MessageForm(request.POST)
        
        if form.is_valid():
            user_message = form.cleaned_data['message']
            
            try:
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
                
                self.message_user(
                    request, 
                    "消息已发送并收到AI回复", 
                    messages.SUCCESS
                )
            except Exception as e:
                self.message_user(
                    request, 
                    f"发送消息时出错: {str(e)}", 
                    messages.ERROR
                )
        
        return HttpResponseRedirect('..')
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['message_form'] = MessageForm()
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
    
    def linked_user(self, obj):
        return format_html(
            '<a href="/admin/core/user/{}/change/">{}</a>',
            obj.user.id,
            obj.user.username
        )
    linked_user.short_description = '所属用户'
    linked_user.admin_order_field = 'user__username'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'conversation_link',
        'content_preview',
        'role_badge',
        'timestamp',
        'linked_user'
    )
    list_filter = ('role', 'timestamp', 'conversation__user')
    search_fields = ('content', 'conversation__id')
    date_hierarchy = 'timestamp'
    list_select_related = ('conversation__user',)
    raw_id_fields = ('conversation',)
    
    # 禁用删除功能
    def has_delete_permission(self, request, obj=None):
        return False
    
    def conversation_link(self, obj):
        return format_html(
            '<a href="/admin/chat_history/conversation/{}/change/">{}</a>',
            obj.conversation.id,
            obj.conversation.id
        )
    conversation_link.short_description = '会话ID'
    conversation_link.admin_order_field = 'conversation__id'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '内容摘要'
    
    def role_badge(self, obj):
        color = {
            'human': '#4CAF50',   # 绿色
            'ai': '#2196F3',      # 蓝色
            'system': '#9C27B0'   # 紫色
        }.get(obj.role, '#607D8B')  # 默认灰色
        return format_html(
            '<span style="color: white; background-color: {};'
            'padding: 2px 8px; border-radius: 10px;">{}</span>',
            color,
            obj.get_role_display()
        )
    role_badge.short_description = '角色'
    role_badge.admin_order_field = 'role'
    
    def linked_user(self, obj):
        return format_html(
            '<a href="/admin/core/user/{}/change/">{}</a>',
            obj.conversation.user.id,
            obj.conversation.user.username
        )
    linked_user.short_description = '所属用户'
    linked_user.admin_order_field = 'conversation__user__username'