from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
# from blog.views import router

from blog.views import *

urlpatterns = [
    path('admin/', admin.site.urls), # admin portal
    path('accounts/', include('allauth.urls')), # all_auth for social login
    # rest_framework
    path('posts/', include('blog.urls')),
    # graphql using graphene-django
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),

    
    # blog app using given paths
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