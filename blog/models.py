"""Models for project."""

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


class Post(models.Model):
    """Model that represents post in our blog."""

    author = models.ForeignKey('auth.User',
                               verbose_name=_(u'Author'),
                               on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_(u'Title'), max_length=200)
    text = models.TextField(verbose_name=_(u'Text'),)
    created_date = models.DateTimeField(verbose_name=_(u'Created date'),
                                        default=timezone.now)
    published_date = models.DateTimeField(verbose_name=_(u'Published date'),
                                          blank=True,
                                          null=True)

    def publish(self):
        """Publish the post."""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        """Render the post instance as a string."""
        return self.title
