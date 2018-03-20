from django.forms import ModelForm, Form
from . import models
from django.db.models import CharField


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
