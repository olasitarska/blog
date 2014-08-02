from django.test import TestCase
from django.core.urlresolvers import reverse

from posts.models import Post

class PostsViewsTestCase(TestCase):

    fixtures = ['posts_views_testdata.json']

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
        post = Post.objects.get(pk=1)
        resp = self.client.get(reverse('posts:post_detail', kwargs={'post_pk':post.pk, 'slug':post.slug}))
        self.assertEqual(resp.status_code, 404)

        # Access published post
        post = Post.objects.get(pk=2)
        resp = self.client.get(reverse('posts:post_detail', kwargs={'post_pk':post.pk, 'slug':post.slug}))
        self.assertEqual(resp.status_code, 200)

        # Access post that does not exists
        resp = self.client.get(reverse('posts:post_detail', kwargs={'post_pk':3, 'slug':'test'}))
        self.assertEqual(resp.status_code, 404)

        # Access post with wrong slug
        resp = self.client.get(reverse('posts:post_detail', kwargs={'post_pk':post.pk, 'slug':'a'}))
        self.assertEqual(resp.status_code, 302)
