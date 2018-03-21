from django.forms import ModelForm, Form
from . import models
from django.db.models import CharField, TextField


class TagsForm(ModelForm):

    class Meta:
        model = models.Tags
        fields = ['name']


class TagsDetailForm(Form):
    name = CharField(max_length=32, blank=True)


class CategoryForm(ModelForm):

    class Meta:
        model = models.Category
        fields = ['name']


class CategoryDetailForm(Form):
    name = CharField(max_length=32, blank=True)


class ArticleForm(ModelForm):

    class Meta:
        model = models.Article
        fields = ['title', 'category', 'author', 'abstract', 'content']


class ArticleDetailForm(Form):
    title = CharField(max_length=128, blank=True)
    abstract = CharField(max_length=512, blank=True)
    content = TextField(blank=True)


class ArticleUserForm(Form):
    username = CharField(max_length=128)
