from django.db import models
from rest_framework.authtoken.models import Token


class User(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    authorization_level = models.IntegerField()


class UserToken(Token):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=256)
