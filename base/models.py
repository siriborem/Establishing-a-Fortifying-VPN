from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Configuration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    configuration = models.CharField(max_length=255, default='None')
    ip_address = models.CharField(max_length=255, default='127.0.0.1')
    is_connected = models.BooleanField(default=False)

    def __str__(self):
        self.user.username
