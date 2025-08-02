from django.db import models
from rest_framework.fields import CharField


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length=200)

    def __str__(self):
        return self.title