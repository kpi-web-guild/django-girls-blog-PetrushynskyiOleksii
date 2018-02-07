"""Models for project."""

from django.db import models
from django.utils import timezone


class Post(models.Model):
    """Model that represents post in our blog."""

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        """Publish the post."""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        """Return title of Post."""
        return self.title
