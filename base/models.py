from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Document(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=true)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=true)
    name = models.CharField(max_length=200)
    description = model.TextField(null=True, blank=True)
