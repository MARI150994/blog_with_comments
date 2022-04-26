from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Article, Comment


# crete comment for article
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


# this serializer called from ArticleDetailSerializer, create hierarchical data for article detail
class CommentHierarchySerializer(serializers.HyperlinkedModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'parent_id', 'url', 'content', 'created', 'level', 'children']

    def get_children(self, comment):
        # we must show comments only to 3 level on article page (in our 'mptt' case to 2 level)
        # we serialize only <= 1 level (because in this case 2 'mptt' level will be show)
        if comment.level <= 1:
            return CommentHierarchySerializer(
                comment.get_children(), many=True,
                context={'request': self.context.get('request')}
            ).data
        # crete link for children of comment with 3 level (in mptt 2 level)
        else:
            # return link for children if there are children
            if comment.get_children():
                request = self.context.get('request')
                return request.build_absolute_uri(comment.get_absolute_url())
            # if no children return null
            else:
                return []


# create comment for comment
class ReplyCreateSerializer(serializers.HyperlinkedModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'parent_id', 'url', 'content', 'created', 'level', 'children']
        read_only_fields = ['id', 'url', 'created', 'level', 'children', 'parent_id']

    def get_children(self, comment):
        # instead of CommentHierarchySerializer now we should show all children
        return ReplyCreateSerializer(
            comment.get_children(), many=True,
            context={'request': self.context.get('request')}
        ).data

    def create(self, validated_data):
        article = self.context['article']
        parent = self.context['parent']
        validated_data.update(
            {'article': article,
             'parent': parent}
        )
        return Comment.objects.create(**validated_data)


# show list of article and create new article
class ArticleListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'created', 'url']
        extra_kwargs = {'content': {'write_only': True}}


# show comments hierarchy to 3 level (in mptt to 2 level)
class ArticleDetailSerializer(serializers.ModelSerializer):
    # show only comments on <= 2 level (level start from 0)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['title', 'content', 'created', 'comments']

    def get_comments(self, article):
        # show comments with level 0 because we use tree structure serializer
        # and don't want repeat subcomments with another level
        comments = Comment.objects.filter(article=article).filter(level=0)
        serializer = CommentHierarchySerializer(
            instance=comments, many=True,
            context={'request': self.context.get('request')}
        )
        return serializer.data
