from datetime import datetime

from django.db.models import F, Count
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter

from social.models import Profile, Subscription, Post
from social.permissions import IsAdminOrIfAuthenticatedReadOnly

from social.serializers import (
    ProfileSerializer,
    SubscriptionSerializer,
    PostSerializer,
    ProfileDetailsSerializer,
    PostDetailSerializer,
    PostListSerializer
)

@extend_schema(
    parameters=[
        OpenApiParameter(
            "username",
            type={"type": "list", "items": {"type": "chars"}},
            description="Filter by username (ex. ?username=username)"
        )
    ]
)
class ProfileViewSet(
    viewsets.ModelViewSet
):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """Allows user to search by username"""
        username = self.request.query_params.get("username")

        queryset = self.queryset

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProfileDetailsSerializer
        return ProfileSerializer


class SubscribersViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user.id)


class TargetsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(target=self.request.user.id)

@extend_schema(
    parameters=[
        OpenApiParameter(
            "message",
            type={"type": "list", "items": {"type": "chars"}},
            description="Filter by contains word in message (ex. ?message=word)"
        )
    ]
)
class PostViewSet(
    viewsets.ModelViewSet
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_queryset(self):
        """Allows user to see only his and followers posts"""
        subs_id_posts = Subscription.objects.filter(
            subscriber__id=self.request.user.id
        ).values_list("id", flat=True)
        
        message_part = self.request.query_params.get("message")
        
        queryset = Post.objects.filter(user_profile__in=subs_id_posts)
        
        if message_part:
            queryset = queryset.filter(message__icontains=message_part)
            

        return queryset.distinct()
    
        
            

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer
