from django.urls import path
from . import views

urlpatterns = [
    path('permission/', views.PermissionView.as_view()),
]
