from django.conf import settings
from django.db import models
#👇这个引用是为了方便做表单的校验
from django.core.validators import MinValueValidator
from django.core.validators import FileExtensionValidator


class Conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    ROLE_CHOICES = [
        ('system', 'System'),
        ('human', 'User'),
        ('ai', 'Assistant'),
    ]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']



        

        
            


    



