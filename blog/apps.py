"""Configuration of app."""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BlogConfig(AppConfig):
    """Configuration for Blog app."""

    name = 'blog'
    vebose_name = _(u'Django Girls blog')
