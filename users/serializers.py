from django.db import models
from rest_framework.serializers import ModelSerializer
from rest_framework.utils import field_mapping
from .models import CustomUser

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'last_login', 'date_joined', 'is_staff')
        