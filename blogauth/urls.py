from django.urls import path
from . import views

urlpatterns = [
    path('permission/', views.PermissionView.as_view()),
    path('permission/<int:id>/', views.PermissionDetailView.as_view()),
    path('group/', views.GroupView.as_view()),
    path('group/<int:id>/', views.GroupDetailView.as_view()),
    path('group/<int:id>/permission/', views.GroupPermissionView.as_view()),
    path('user/', views.UserView.as_view()),
    path('user/<int:id>/', views.UserDetailView.as_view()),
    path('user/<int:id>/permission/', views.UserPermissionView.as_view()),
]
