# blog/schema.py
from django.db.models import query
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User

from blog.models import Post

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", 'email', 'posts')

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "user", "title", "slug", "content", "image", 'created', 'updated')

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    # posts_by_query = graphene.Field(PostType, query=graphene.String(required=True))
    category_by_name = graphene.Field(UserType, name=graphene.String(required=True))
    def resolve_all_posts(root, info):
        # We can easily optimize query count in the resolve method
        return Post.objects.select_related("user").all()
    def resolve_category_by_name(root, info, name):
        try:
            return User.objects.get(username=name)
        except User.DoesNotExist:
            return None
    # def resolve_posts_by_query(root, info, query):
    #     return Post.objects.filter(title__icontains = query)

schema = graphene.Schema(query=Query)