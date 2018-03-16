from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    username = models.CharField(unique=True, max_length=128)
    password = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)
    email = models.EmailField()
    user_info = models.OneToOneField(UserInfo)
    group = models.ManyToManyField(Group)
    permission = models.ManyToManyField(Permission)


class UserInfo(models.Model):
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)
    nick_name = models.CharField(max_length=128, blank=True)
    gender = models.CharField(max_length=1, default='s', choices=(('male', 'm'), ('female', 'f'), ('secret', 's')))
    intruduction = models.CharField(max_length=256, blank=True)


class Group(models.Model):
    name = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)
    permission = models.ManyToManyField(Permission)


class Permission(models.Model):
    name = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)


class Article(models.Model):
    title = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASECADE)
    category = models.ForeignKey(Category, on_delete=models.CASECADE)
    tags = models.ManyToManyField(Tags)
    abstract = models.CharField(max_length=512)
    content = models.TextField()
    likes = models.OneToOneField(Likes)


class Category(models.Model):
    name = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)


class Tags(models.Model):
    name = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)


class Commit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASECADE)
    article = models.ForeignKey(Article, on_delete=CASECADE)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)
    content = models.TextField()


class Likes(models.Model):
    readers = models.IntegerField()
    agree = models.ManyToManyField(User)
    disagree = models.ManytoManyField(User)
