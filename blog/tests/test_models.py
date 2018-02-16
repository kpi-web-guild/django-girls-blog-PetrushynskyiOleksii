"""Tests for models."""

from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Post


class PostModelTest(TestCase):
    """Tests for post model."""

    def setUp(self):
        """Init test data."""
        self.user = User.objects.create(username='UserTest')
        self.test_post = Post.objects.create(author=self.user,
                                             title='Title Test',
                                             text='Text Test 123 !@#')

    def tearDown(self):
        """Delete test data."""
        del self.user
        del self.test_post

    def test_post_publish(self):
        """Post published successfully."""
        self.test_post.publish()

    def test_post_str(self):
        """Post is rendered as its title."""
        self.assertEqual(str(self.test_post), 'Title Test')
