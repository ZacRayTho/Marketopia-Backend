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

class Review(models.Model):
    # limit the integerField on the front end to only allow 1-5
    rating = models.IntegerField()
    seller = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='seller')

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    price = models.IntegerField()
    seller = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.PROTECT, related_name='listing')
    category = models.ManyToManyField('Category')
    
class Image(models.Model):
    pic = models.URLField()
    owner = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='Image', default=1)

class Location(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name