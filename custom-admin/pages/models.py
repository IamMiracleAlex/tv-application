from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    pass


class UserMetric(User):

    class Meta:
        proxy = True
        verbose_name_plural = 'User Metrics'



class MassMail(models.Model):
    subject = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name_plural = "Mass Mail"


