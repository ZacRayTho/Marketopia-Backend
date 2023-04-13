from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

class Message(models.Model):
    text = models.TextField()
    viewed = models.BooleanField()
    date_time_sent = models.TimeField()
    sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='recipient')