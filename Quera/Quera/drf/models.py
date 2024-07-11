from django.db import models
from rest_framework.authtoken.models import Token


class MyModel(models.Model):
    pass


class User(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

