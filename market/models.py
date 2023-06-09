from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    image = models.URLField(default="https://media.istockphoto.com/id/1074273158/vector/person-gray-photo-placeholder-man.jpg?s=612x612&w=0&k=20&c=OcUd-R2-sPpl33QVLuY9haUUAuvdlQK8XrkciaNFLO8=")
    saved = models.ManyToManyField('Listing')
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta(AbstractUser.Meta):
        ordering = ["-date_joined"]
        db_table = "users"

class Message(models.Model):
    text = models.TextField()
    viewed = models.BooleanField()
    date_time_sent = models.BigIntegerField()
    timestamp = models.CharField(max_length=50, default="bad")
    sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='recipient')

class Review(models.Model):
    # limit the integerField on the front end to only allow 1-5
    rating = models.IntegerField()
    seller = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='seller')
    reviewer = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='reviewer', default=1)

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    price = models.IntegerField()
    seller = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, related_name='listing', null=True)
    category = models.ManyToManyField('Category')
    
    def __str__(self):
        return f"{self.seller}'s {self.title}"
    
class Image(models.Model):
    pic = models.URLField()
    owner = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='Image', default=1)

    def __str__(self):
        return self.pic

class Location(models.Model):
    city = models.CharField(max_length=100, default="Something")
    state = models.CharField(max_length=100, default="Went Wrong")
    zip = models.IntegerField(default="0")
    lat = models.FloatField(default="0")
    long = models.FloatField(default="0")

    def __str__(self):
        return self.city + ", " + self.state

class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name