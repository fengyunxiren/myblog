from django.db import models
from django.utils import timezone
from blogauth import models as amodels

# Create your models here.


class Likes(models.Model):
    readers = models.IntegerField(default=0)
    like = models.ManyToManyField(amodels.User, related_name="like_user")
    disagree = models.ManyToManyField(
        amodels.User, related_name="disagree_user")


class Tags(models.Model):
    name = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)


class Article(models.Model):
    title = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)
    author = models.ForeignKey(amodels.User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    abstract = models.CharField(max_length=512)
    content = models.TextField()
    likes = models.OneToOneField(Likes, on_delete=models.CASCADE)


class Commit(models.Model):
    user = models.ForeignKey(amodels.User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=timezone.now())
    update_time = models.DateTimeField(auto_now=timezone.now())
    is_delete = models.BooleanField(default=False)
    content = models.TextField()
