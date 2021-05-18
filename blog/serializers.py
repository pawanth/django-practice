from django.contrib.auth.models import User
from rest_framework import serializers
import base64
import uuid
from django.core.files.base import ContentFile
from .models import Post


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
                # base64 encoded image - decode
                format, imgstr = data.split(';base64,') # format ~= data:image/X,
                ext = format.split('/')[-1] # guess file extension
                id = uuid.uuid4()
                data = ContentFile(base64.b64decode(imgstr), name = id.urn[-9:] + '.' + ext)
        else:
            print("something wrong")
        return super(Base64ImageField, self).to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='owner.username')
    image = Base64ImageField(required=False)
    class Meta:
        model = Post
        fields = ('id',  'user', 'title', 'slug', 'image', 'content')
        read_only_fields = ('updated', 'user', 'slug')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']