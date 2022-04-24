from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Article, Comment


class ArticleListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'created', 'url']


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'created']

    # bind comment with article
    def create(self, validated_data):
        article_id = self.context['article_id']
        article = get_object_or_404(Article, id=article_id)
        validated_data['article'] = article
        return Comment.objects.create(**validated_data)
