from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class HomeModel(models.Model):
    url = models.URLField(max_length = 200)
    images = models.ImageField(upload_to='static/images',null=True, blank=True)
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = 'notes'
        verbose_name_plural = 'notes'


class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    description = models.TextField()
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)



class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_finished = models.BooleanField(default=False)
