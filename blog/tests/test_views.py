"""Test for views."""

from datetime import datetime

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from ..models import Post


class PostViewTest(TestCase):
    """Test for post views."""

    USERNAME = 'testuser'
    PASSWORD = 'password'

    def setUp(self):
        """Init test data."""
        self.client = Client()
        self.user = User.objects.create(username=self.USERNAME,
                                        email='testuser@test.com',
                                        is_superuser=True,
                                        is_staff=True,
                                        is_active=True)
        self.user.set_password(self.PASSWORD)
        self.user.save()
        self.tz = timezone.get_current_timezone()
        self.post1 = Post.objects.create(author=self.user,
                                         title='Title Test 1',
                                         text='Text Test 123 !@#',
                                         published_date=datetime(day=1, month=1, year=2017, tzinfo=self.tz))
        self.post2 = Post.objects.create(author=self.user,
                                         title='Title Test 2',
                                         text='Text Test 123 !@#',
                                         published_date=datetime(day=2, month=2, year=2011, tzinfo=self.tz))
        self.post3 = Post.objects.create(author=self.user,
                                         title='Title Test 3',
                                         text='Text Test 123 !@#',
                                         published_date=datetime(day=3, month=3, year=2014, tzinfo=self.tz))
        self.future_post = Post.objects.create(author=self.user,
                                               title='Title Test 4',
                                               text='Text Test 123 !@#',
                                               published_date=datetime(day=4, month=4, year=2222, tzinfo=self.tz))

    def tearDown(self):
        """Clean test data."""
        del self.post1
        del self.post2
        del self.post3
        del self.future_post
        del self.tz
        del self.client
        del self.user

    def test_post_list(self):
        """Test list of posts."""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 3)
        self.assertNotContains(response, self.future_post)
        self.assertTemplateUsed(response, 'blog/post_list.html', 'blog/base.html')

    def test_sorting_post_list(self):
        """Test post sorting."""
        response = self.client.get(reverse('post_list'), {'order_by': 'published_date'})
        posts = response.context['posts']
        self.assertEqual(posts[2].published_date, datetime(day=1, month=1, year=2017, tzinfo=self.tz))
        self.assertEqual(posts[1].published_date, datetime(day=3, month=3, year=2014, tzinfo=self.tz))
        self.assertEqual(posts[0].published_date, datetime(day=2, month=2, year=2011, tzinfo=self.tz))

    def test_post_detail_view(self):
        """Test detail page of specific post."""
        response = self.client.get(reverse('post_detail', kwargs={'pk': 9999}))
        self.assertEqual(404, response.status_code)
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post1.pk}))
        self.assertEqual(200, response.status_code)

    def test_post_new_view(self):
        """Test view for add post."""
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.post(reverse('post_new'),
                                    {'author': self.user, 'title': 'Test', 'text': 'superText', },
                                    follow=True)
        self.assertEqual(200, response.status_code)
        self.post = Post.objects.get(author=self.user, title='Test', text='superText')
        self.assertContains(response, self.post)

    def test_post_edit(self):
        """Test view for edit post."""
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_edit', kwargs={'pk': 9999}))
        self.assertEqual(404, response.status_code)
        response = self.client.get(reverse('post_edit', kwargs={'pk': self.post1.pk}))
        self.assertEqual(200, response.status_code)
