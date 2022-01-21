from django.db import models
from django.conf import settings
# Create your models here.


class UserRegistrationModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class UserDetails(models.Model):
    userId = models.IntegerField()
    idValue = models.IntegerField()
    title = models.TextField(max_length=500)
    body = models.TextField(max_length=1000)