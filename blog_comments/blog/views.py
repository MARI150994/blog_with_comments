from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleDetailSerializer, CommentCreateSerializer, ReplyCreateSerializer


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer


class ArticleDetail(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    # add article_id in serializer context
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['article_id'] = self.kwargs.get('pk')
        return context


class ReplyCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = ReplyCreateSerializer

    # add article and parent comment in serializer context
    def get_serializer_context(self):
        context = super().get_serializer_context()
        parent_comment_id = self.kwargs.get('pk')
        parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
        article = parent_comment.article
        context.update(
            {'parent': parent_comment,
             'article': article}
        )
        return context
