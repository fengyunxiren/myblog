from django.forms import ModelForm
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


class GroupForm(ModelForm):
    class Meta:
        model = models.Group
        fields = ['name']
        permissions = CharField(max_length=128)
