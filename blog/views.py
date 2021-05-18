from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from rest_framework import routers, generics, permissions, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, UserSerializer

# Class based views
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

# DRF Views
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

#API Viwes
class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, # permissions.IsAuthenticatedOrReadOnly,
    ]
router = routers.DefaultRouter()
router.register(r'', PostViewSet)
