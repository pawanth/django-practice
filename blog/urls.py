from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import router

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]