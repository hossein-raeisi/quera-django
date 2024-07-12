from django.db import models
from rest_framework.authtoken.models import Token


class User(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    authorization_level = models.IntegerField()

    @property
    def is_active(self):
        return True


class UserToken(Token):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=256)


class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
