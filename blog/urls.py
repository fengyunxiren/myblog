from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('permission/', TemplateView.as_view()),
]