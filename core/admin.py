from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import User
# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # 控制列表显示字段
    list_display = ('username', 'email', 'position', 'age', 'is_staff')
    # 添加自定义字段到过滤选项
    list_filter = ('is_staff', 'is_superuser', 'position')
    # 增强搜索功能
    search_fields = ('username', 'email', 'position')
    # 控制详情页字段分组
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email', 'age')}),
        ('职业信息', {'fields': ('position',)}),
        ('权限管理', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    # 添加自定义字段到管理员添加用户表单
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'position', 'age'),
        }),
    )
    # 按年龄排序
    ordering = ('-date_joined',)

admin.site.register(User, CustomUserAdmin)




