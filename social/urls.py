from django.urls import path, include
from rest_framework import routers

from social.views import (
    ProfileViewSet,
    SubscribersViewSet,
    PostViewSet,
    TargetsViewSet
)

router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("subs", SubscribersViewSet)
router.register("posts", PostViewSet)
router.register("targets", TargetsViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "social"
