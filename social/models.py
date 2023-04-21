from django.db import models
from django.conf import settings


class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    username = models.CharField(max_length=63)
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.username} ({self.first_name} {self.last_name})"


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscribers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'target')
        
    def __str__(self):
        return f"{self.subscriber} -> {self.target} ({self.target.id})"


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    user_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.user_profile.username}  -->  {self.message}"
