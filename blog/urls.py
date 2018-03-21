from django.urls import path
from . import views

urlpatterns = [
    path('tags/', views.TagsView.as_view()),
    path('tags/<int:id>/', views.TagsDetailView.as_view()),
    path('category/', views.CategoryView.as_view()),
    path('category/<int:id>/', views.CategoryDetailView.as_view()),
    path('article/', views.ArticleView.as_view()),
    path('article/<int:id>/', views.ArticleDetailView.as_view()),
    path('article/<int:id>/likes/', views.ArticleLikeView.as_view()),
    path('article/<int:id>/disagree/', views.ArticleDisagreeView.as_view()),
    path('article/<int:id>/tags/', views.ArticleTagsView.as_view()),
]
