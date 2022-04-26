from django.urls import path, include
from . import views

urlpatterns = [
    path('articles/', views.ArticleListCreateAPIView.as_view(), name='article-list'),
    path('articles/<int:pk>/', views.ArticleDetailAPIView.as_view(), name='article-detail'),
    path('articles/<int:pk>/comments/', views.CommentCreateAPIView.as_view(), name='comment-create'),
    # path('articles/<int:art_pk>/comments/<int:pk>', views.CommentCreate.as_view(), name='comment-create'),
    # TODO awful path
    path('comments/<int:pk>', views.ReplyListCreateAPIView.as_view(), name='comment-detail'),
]
