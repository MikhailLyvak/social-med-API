from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from social.models import (
    Profile,
    Subscription,
    Post,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "user", "username", "full_name")


class ProfileDetailsSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "email", "user", "username", "full_name")
    


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "subscriber", "target", "created_at")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "created_at", "message", "user_profile")
        

class PostListSerializer(PostSerializer):
    username = serializers.CharField(source="user_profile.username", read_only=True)
    
    class Meta:
        model = Post
        fields = fields = ("id", "created_at", "message", "user_profile", "username")


class PostDetailSerializer(PostSerializer):
    username = serializers.CharField(source="user_profile.username", read_only=True)
    user_first_name = serializers.CharField(source="user_profile.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user_profile.last_name", read_only=True)
    
    class Meta:
        model = Post
        fields = ("id", "created_at", "message", "username", "user_first_name", "user_last_name")

