"""game_ type class module"""
from django.db import models


class GameType(models.Model):
    """game type model class"""
    label = models.CharField(max_length=50)
    description = models.CharField(max_length=350)
