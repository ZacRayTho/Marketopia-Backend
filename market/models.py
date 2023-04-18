from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    def __str__(self):
        return str(self.email)

    class Meta(AbstractUser.Meta):
        ordering = ["-date_joined"]
        db_table = "users"

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
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, related_name='listing', null=True)
    category = models.ManyToManyField('Category')
    
class Image(models.Model):
    pic = models.URLField()
    owner = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='Image', default=1)

    def __str__(self):
        return self.pic

class Location(models.Model):
    city = models.CharField(max_length=100, default="Something")
    state = models.CharField(max_length=100, default="Went Wrong")
    zip = models.IntegerField(default="0")

    def __str__(self):
        return self.city + ", " + self.state

class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name