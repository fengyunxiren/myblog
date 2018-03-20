from django.forms import Form
from django.db.models import CharField


class DeleteForm(Form):
    real = CharField(max_length=5, default="False", choices=["True", "False"])
