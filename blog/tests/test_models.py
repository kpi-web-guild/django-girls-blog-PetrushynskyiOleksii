"""Tests for models."""
from datetime import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from blog.models import Post


class PostModelTest(TestCase):
    """Tests for post model."""

    def setUp(self):
        """Pre-populate test data."""
        self.user = User.objects.create(username='UserTest')
        self.test_post = Post.objects.create(author=self.user,
                                             title='Title Test',
                                             text='Text Test 123 !@#')

    def tearDown(self):
        """Clean-up test data."""
        del self.user
        del self.test_post

    @patch('django.utils.timezone.now', lambda: datetime(day=1,
                                                         month=1,
                                                         year=2017,
                                                         tzinfo=timezone.get_current_timezone()))
    def test_post_publish(self):
        """Post published successfully."""
        self.test_post.publish()
        self.assertEqual(self.test_post.published_date, datetime(day=1,
                                                                 month=1,
                                                                 year=2017,
                                                                 tzinfo=timezone.get_current_timezone()))

    def test_post_str(self):
        """Post is rendered as its title."""
        self.assertEqual(str(self.test_post), 'Title Test')
