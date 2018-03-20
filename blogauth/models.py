from django.db import models
from django.utils import timezone

# Create your models here.
STRFORMAT = "%Y-%m-%dT%H:%M:%S.%f%Z"

class Permission(models.Model):
    name = models.CharField(max_length=128, unique=True)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)
    permission = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)
    nick_name = models.CharField(max_length=128, blank=True, default="")
    gender = models.CharField(max_length=1, default='s', choices=(
        ('male', 'm'), ('female', 'f'), ('secret', 's')))
    intruduction = models.CharField(max_length=256, blank=True, default="")


class User(models.Model):
    username = models.CharField(unique=True, max_length=128)
    password = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)
    email = models.EmailField()
    user_info = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    group = models.ManyToManyField(Group)
    permission = models.ManyToManyField(Permission)
