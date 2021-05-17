from blog.serializers import PostSerializer
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns

from blog.views import ( 
    BlogListView, 
    BlogDetailView, 
    BlogCreateView, 
    BlogUpdateView, 
    BlogDeleteView
)

# path('', include(('xyz.urls', 'xyz'), namespace='xyz'))
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from blog.views import PostList, PostDetail
from blog.serializers import PostSerializer
from blog.models import Post
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

# django-graphene
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name="blog/base.html")),

    # all_auth app
    path('accounts/', include('allauth.urls')),
    
    # rest_framework
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # graphql using graphene-django
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),

    # blog app
    path('', include(([
        path('logout', LogoutView.as_view(), name='logout'),
        path('',  BlogListView.as_view(), name='blog-list'),
        path('create/', BlogCreateView.as_view(), name='create'),
        path('<slug:slug>/',  BlogDetailView.as_view(), name='retrieve'),
        path('<slug:slug>/edit/',  BlogUpdateView.as_view(), name='update'),
        path('<slug:slug>/remove/',  BlogDeleteView.as_view(), name='delete'),
    ], 'blog'), namespace='blog')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = format_suffix_patterns(urlpatterns)