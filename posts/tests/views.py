from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from posts.models import Post

class PostsViewsTestCase(TestCase):

    fixtures = ['posts_views_testdata.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.user.set_password('o')
        self.user.save()
        self.post_1 = Post.objects.get(pk=1)
        self.post_2 = Post.objects.get(pk=2)

    def test_post_list(self):
        # Access homepage
        resp = self.client.get(reverse('posts:post_list'))
        self.assertEqual(resp.status_code, 200)

        # Check if it returns a list of posts
        self.assertTrue('post_list' in resp.context)

        # Is post on the list?
        self.assertEqual([post.pk for post in resp.context['post_list']], [2])

        # Check if there is no pagination
        self.assertFalse('post_list.has_next' in resp.context)
        self.assertFalse('post_list.has_prev' in resp.context)

    def test_post_detail(self):
        # Access unpublished post
        resp = self.client.get(reverse('posts:post_detail', kwargs={'post_pk':self.post_1.pk, 'slug':self.post_1.slug}))
        self.assertEqual(resp.status_code, 404)

        # Access published post
        resp = self.client.get(reverse('posts:post_detail', kwargs={'post_pk':self.post_2.pk, 'slug':self.post_2.slug}))
        self.assertEqual(resp.status_code, 200)

        # Access post that does not exists
        resp = self.client.get(reverse('posts:post_detail', kwargs={'post_pk':3, 'slug':'test'}))
        self.assertEqual(resp.status_code, 404)

        # Access post with wrong slug
        resp = self.client.get(reverse('posts:post_detail', kwargs={'post_pk':self.post_2.pk, 'slug':'a'}))
        self.assertEqual(resp.status_code, 302)

    def test_post_toggle_publish(self):
        # Check if post isn't public
        self.assertFalse(Post.objects.get(pk=1).is_public())

        # Login and perform a request
        self.client.login(username='olasitarska', password='o')
        response = self.client.get(reverse('posts:post_toggle_publish', kwargs={'post_pk': 1}))
        self.assertEqual(response.status_code, 302)

        # Check if post is public
        self.assertTrue(Post.objects.get(pk=1).is_public())

        # Modify again
        response = self.client.get(reverse('posts:post_toggle_publish', kwargs={'post_pk': 1}))
        self.assertEqual(response.status_code, 302)

        # Check if post isn't public
        self.assertFalse(Post.objects.get(pk=1).is_public())

    def test_post_remove(self):
        # Create post:
        post = Post.objects.create(author=self.user, title='To remove', content='b')
        self.assertTrue(Post.objects.filter(title='To remove').exists())

        # Perform a request
        self.client.login(username='olasitarska', password='o')
        response = self.client.get(reverse('posts:post_remove', kwargs={'post_pk': post.pk}))
        self.assertEqual(response.status_code, 302)

        # Check if post does not exist anymore:
        self.assertFalse(Post.objects.filter(title='To remove').exists())
