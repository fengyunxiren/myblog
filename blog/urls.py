from django.urls import path
from . import views

urlpatterns = [
    path('tags/', views.TagsView.as_view()),
    path('tags/<int:id>/', views.TagsDetailView.as_view()),
    path('category/', views.CategoryView.as_view()),
]
