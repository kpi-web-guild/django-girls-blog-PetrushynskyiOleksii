"""Test for views."""
from datetime import datetime
from unittest.mock import patch

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from ..models import Post


class PostViewTest(TestCase):
    """Test for post views."""

    USERNAME = 'testuser'
    PASSWORD = 'password'
    EMAIL = 'email@test.com'

    def setUp(self):
        """Pre-populate test data."""
        self.client = Client()
        self.user = User.objects.create_superuser(username=self.USERNAME,
                                                  password=self.PASSWORD,
                                                  email=self.EMAIL,
                                                  )
        self.tz = timezone.get_current_timezone()
        self.first_post = Post.objects.create(author=self.user,
                                              title='Title Test 1',
                                              text='Text Test 123 !@#',
                                              published_date=datetime(day=1, month=1, year=2017, tzinfo=self.tz))
        self.second_post = Post.objects.create(author=self.user,
                                               title='Title Test 2',
                                               text='Text Test 123 !@#',
                                               published_date=datetime(day=2, month=2, year=2011, tzinfo=self.tz))
        self.third_post = Post.objects.create(author=self.user,
                                              title='Title Test 3',
                                              text='Text Test 123 !@#',
                                              published_date=datetime(day=3, month=3, year=2014, tzinfo=self.tz))
        self.future_post = Post.objects.create(author=self.user,
                                               title='Title Test 4',
                                               text='Text Test 123 !@#',
                                               published_date=datetime(day=4, month=4, year=2222, tzinfo=self.tz))

    def tearDown(self):
        """Clean-up test data."""
        del self.first_post
        del self.second_post
        del self.third_post
        del self.future_post
        del self.tz
        del self.client
        del self.user

    def test_post_list(self):
        """Test list of posts."""
        with patch('django.utils.timezone.now', lambda: datetime(day=1, month=1, year=2018, tzinfo=self.tz)):
            response = self.client.get(reverse('post_list'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'blog/post_list.html', 'blog/base.html')
            self.assertEqual(len(response.context['posts']), 3)
            self.assertNotContains(response, self.future_post)

    def test_sorting_post_list(self):
        """Test post sorting."""
        response = self.client.get(reverse('post_list'), {'order_by': 'published_date'})
        posts = response.context['posts']
        with patch('django.utils.timezone.now', lambda: datetime(day=1, month=1, year=2018, tzinfo=self.tz)):
            self.assertEqual(posts[2].published_date, datetime(day=1, month=1, year=2017, tzinfo=self.tz))
            self.assertEqual(posts[1].published_date, datetime(day=3, month=3, year=2014, tzinfo=self.tz))
            self.assertEqual(posts[0].published_date, datetime(day=2, month=2, year=2011, tzinfo=self.tz))
            self.assertNotContains(response, self.future_post)

    def test_post_detail_view(self):
        """Test detail page of specific post."""
        response = self.client.get(reverse('post_detail', kwargs={'pk': 9999}))
        self.assertEqual(404, response.status_code)
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.first_post.pk}))
        self.assertEqual(200, response.status_code)

    def test_post_new_view(self):
        """Test view for add post."""
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.post(reverse('post_new'),
                                    {'author': self.user,
                                     'title': 'Test New Post',
                                     'text': 'Test Text',
                                     },
                                    follow=True)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Test New Post')

    def test_post_edit(self):
        """Test view for edit post."""
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_edit', kwargs={'pk': 9999}))
        self.assertEqual(404, response.status_code)
        response = self.client.get(reverse('post_edit', kwargs={'pk': self.first_post.pk}))
        self.assertEqual(200, response.status_code)
        response = self.client.post(reverse('post_edit', kwargs={'pk': self.first_post.pk}),
                                    {'author': self.user,
                                     'title': 'Test Title Edit',
                                     'text': 'Test Text Edit',
                                     },
                                    follow=True)
        self.assertContains(response, 'Test Text Edit')
        self.assertEqual(200, response.status_code)

    def test_drafts(self):
        """Test view for drafts."""
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_draft_list'))
        self.assertEqual(200, response.status_code)

    def test_publish_post(self):
        """Test for publishing post."""
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        post = Post.objects.create(author=self.user, title='Test Publish', text='Text Publish')
        response = self.client.get(reverse('post_publish', kwargs={'pk': post.pk}), follow=True)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': post.pk}))
