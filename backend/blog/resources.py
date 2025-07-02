from import_export import resources
from .models import (
    Post,
    Category,
    Tag,
    Comment,
)

class PostResource(resources.ModelResource):
    class Meta:
        model = Post

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class TagResource(resources.ModelResource):
    class Meta:
        model = Tag


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment