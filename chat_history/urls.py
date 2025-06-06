from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet,basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]










