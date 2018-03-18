from django.urls import path
from . import views

urlpatterns = [
    path('permission/', views.PermissionView.as_view()),
    path('permission/<int:id>/', views.PermissionDetailView.as_view()),
    path('group/', views.GroupView.as_view()),
]
