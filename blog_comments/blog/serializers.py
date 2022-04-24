from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Article, Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'created']

    # bind comment with article
    def create(self, validated_data):
        article_id = self.context['article_id']
        article = get_object_or_404(Article, id=article_id)
        validated_data['article'] = article
        return Comment.objects.create(**validated_data)


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'created']

    # bind comment with article
    def create(self, validated_data):
        article = self.context['article']
        parent = self.context['parent']
        validated_data.update(
            {'article': article,
             'parent': parent}
        )
        return Comment.objects.create(**validated_data)


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created', 'level', 'parent', 'children']


class ArticleListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'created', 'url']


class ArticleDetailSerializer(serializers.ModelSerializer):
    # comments = CommentDetailSerializer(many=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['title', 'content', 'comments']

    def get_comments(self, article):
        comments = Comment.objects.filter(article=article).filter(level__lte=2)
        serializer = CommentDetailSerializer(instance=comments, many=True)
        return serializer.data
