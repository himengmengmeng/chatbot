from functools import partial, partialmethod
from typing import Any
from unittest import case
from django.db.models import Count, Sum, Case, When, IntegerField
from django.contrib import admin
from django.db.models.query import QuerySet
from django.forms import IntegerField
from django.http.request import HttpRequest
from.import models
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



# 内联显示 Message（在 Conversation 详情页）
class MessageInline(admin.TabularInline):  # 或者 StackedInline 以不同样式显示
    model = Message
    extra = 0  # 不显示空表单
    fields = ('role', 'content', 'timestamp')  # 显示的字段
    readonly_fields = ('timestamp',)  # 时间戳不可编辑
   

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'linked_user', 'created_at')
    list_display_links = ('id',)  # 使 ID 可点击进入详情页
    inlines = [MessageInline]  # 关键：内联显示 Message
    
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'id')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user',)  # 优化用户选择框
    
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
    
    def conversation_link(self, obj):
        return format_html(
            '<a href="/admin/chat_app/conversation/{}/change/">{}</a>',
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


















