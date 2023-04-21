from django.contrib import admin

from social.models import (
    Profile,
    Subscription,
    Post,
)

admin.site.register(Profile)
admin.site.register(Subscription)
admin.site.register(Post)
