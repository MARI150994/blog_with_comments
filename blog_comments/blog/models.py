from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Article model
class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Article: {self.title}'

    class Meta:
        ordering = ['-created']


# Comment model, for hierarchical structure of comments use django-mptt
class Comment(MPTTModel):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    # this field requires django-mptt
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    def __str__(self):
        return f'Comment {self.id} for article: {self.article}'

    class MPTTMeta:
        order_insertion_by = ['-created']
