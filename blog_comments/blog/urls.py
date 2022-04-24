from django.urls import path, include
from . import views

urlpatterns = [
    path('articles/', views.ArticleList.as_view(), name='article-list'),
    path('articles/<int:pk>', views.ArticleDetail.as_view(), name='article-detail'),
    path('articles/<int:pk>/comments', views.CommentCreate.as_view(), name='comment-create'),
]
