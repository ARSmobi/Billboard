from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'gender', 'birthday')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('id', 'user', 'title', 'text', 'category')


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'user', 'advertisement', 'text')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'text')
