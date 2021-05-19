from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene
from django.contrib.auth.models import User
from .models import Post


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['id']
        interfaces = (relay.Node, )

class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'content': ['exact', 'icontains'],
            'user': ['exact'],
            'user_id' : ['exact'],
        }
        interfaces = (relay.Node, )
class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'

class Query(ObjectType):
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)

    post = relay.Node.Field(PostNode)
    all_posts = DjangoFilterConnectionField(PostNode)

class PostMutation(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=False)
        content = graphene.String(required=False)
        id = graphene.ID(required=False)
        delete = graphene.Boolean()
    post = graphene.Field(PostType)
    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, 
                                id=None, delete=False, **kwargs):
        if not id:
            # Create post
            print('Creating post')
            post = Post.objects.create(
                title = kwargs.get('title'),
                content = kwargs.get('content')
            )
            return PostMutation(post=post)
        else:
            post = Post.objects.get(pk=from_global_id(id)[1])
            if delete:
                # delete post
                print('Deleting post')
                post.delete()
                return cls(ok=True)
            else:
                # Update post 
                print('Updating post')
                post.title = kwargs.get('title')
                post.content = kwargs.get('content')
                post.save()
                return PostMutation(post=post)


class Mutation(ObjectType):
    mutate_post = PostMutation.Field()