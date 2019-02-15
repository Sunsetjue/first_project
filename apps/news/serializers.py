from apps.cms.models import NewsCategory,News
from rest_framework import serializers
from apps.project.models import User
from .models import Comment
from apps.news.models import Carousel

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ("id", "name")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ("uid", "telephone", "username", "email", "is_staff", "is_active")

class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializer()
    class Meta:
        model = News
        fields = ("id", "title", "describe", "thumbnail", "category", "author", "timer")

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = ("id", "comment", "author", "pub_time")

class CarouselSerializers(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = ("id", "image_url", "link_to", "position")