"""Views for blog app."""

from django.shortcuts import render


def post_list(request):
    """Render the post list view."""
    return render(request, 'blog/post_list.html', {})
