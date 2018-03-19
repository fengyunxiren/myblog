from django.forms import ModelForm, Form
from django.db.models import CharField
from . import models


class PermissionForm(ModelForm):
    class Meta:
        model = models.Permission
        fields = ['name', ]


class PermissionUpdateForm(ModelForm):
    class Meta:
        model = models.Permission
        fields = ['id', 'name']


class PermisssionDeleteForm(ModelForm):
    class Meta:
        model = models.Permission
        fields = ['id']
        real = CharField(max_length=5, default="False")


class GroupForm(ModelForm):
    class Meta:
        model = models.Group
        fields = ['name']
        permissions = CharField(max_length=128)


class GroupUpdateForm(ModelForm):
    class Meta:
        model = models.Group
        fields = ['id', 'name']


class GroupDeleteForm(ModelForm):
    class Meta:
        model = models.Group
        fields = ['id']
        real = CharField(max_length=5, default="False")


class GroupPermissionForm(Form):
    name = CharField(max_length=128)
