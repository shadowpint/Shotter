from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from .models import *


class UrlSerializer(serializers.ModelSerializer):

    class Meta:

        model = Urls
        fields = '__all__'