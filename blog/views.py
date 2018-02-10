"""Views for blog app."""

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post
from .forms import PostForm


def post_list(request):
    """Render page with list of posts."""
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    """Render page with details of specific post."""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    """Render page with form of post."""
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
