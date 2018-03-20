from django.forms import ModelForm, Form
from django.db.models import CharField, EmailField
from . import models


class PermissionForm(ModelForm):

    class Meta:
        model = models.Permission
        fields = ['name', ]


class PermissionDetailForm(Form):
    name = CharField(max_length=128, blank=True)


class GroupForm(ModelForm):

    class Meta:
        model = models.Group
        fields = ['name']
        permissions = CharField(max_length=128)


class GroupDetailForm(Form):
    name = CharField(max_length=128, blank=True)


class UserForm(ModelForm):

    class Meta:
        model = models.User
        fields = ["username", "password", "email"]


class UserDetailForm(Form):
    password = CharField(max_length=64, blank=True)
    email = EmailField(blank=True)


class UserInfoDetailForm(Form):
    nick_name = CharField(max_length=128, blank=True, default="")
    gender = CharField(max_length=1, default='s', choices=(
        ('male', 'm'), ('female', 'f'), ('secret', 's')), blank=True)
    intruduction = CharField(max_length=256, blank=True, default="")


class DeleteForm(Form):
    real = CharField(max_length=5, default="False", choices=["True", "False"])
