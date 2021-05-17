from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib import messages
from urllib.parse import quote_plus

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post
from .forms import PostForm
# Create your views here.

class BlogListView(ListView):
    model = Post
    context_object_name = 'instances'  # default object_list
    paginate_by = 10  # if pagination is desired
    template_name = 'blog/blog_homepage.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog|home'
        return context

class BlogDetailView(DetailView):
    model = Post
    # context_object_name = 'instance'  # default object_list
    # default template_name = 'post_Detail'
    # defautl context_object_name = 'post' or 'instance'

class BlogCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    # default templage_name = 'blog/post_form'

class BlogUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'blog/post_form.html'
    # template_name_suffix = '_update_form'

class BlogDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:blog-list')


from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.contrib import messages
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
from django.shortcuts import render, get_object_or_404,redirect 
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from blog.models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer

#API Viwes
class PostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
