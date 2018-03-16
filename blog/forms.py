from django.forms import ModelForm
from . import models

class PermissionForm(ModelForm):
    class Meta:
        model = models.Permission
        fields = ['name', ]

class PermissionUpdateForm(ModelForm):
    class Meta:
        model = models.Permission
        fields = ['id', 'name']