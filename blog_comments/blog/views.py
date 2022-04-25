from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleDetailSerializer, CommentCreateSerializer, ReplyCreateSerializer


# get list of articles, create new article
class ArticleCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer


# show article detail and all comment for this article (to 3 level)
class ArticleDetailAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer


# create comment for article (1 level comment, in mptt 0 level)
class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    # add article_id in serializer context
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['article_id'] = self.kwargs.get('pk')
        return context


# create reply on comments, show all subcomments
class ReplyListCreateAPIView(generics.ListCreateAPIView):
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

    # if get method we will return only children of this comment
    def get_queryset(self):
        comment_pk = self.kwargs.get('pk')
        comment = get_object_or_404(Comment, id=comment_pk)
        return Comment.objects.filter(parent=comment)
