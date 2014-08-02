from django.test import TestCase


class PostsViewsTestCase(TestCase):

    fixtures = ['posts_views_testdata.json']

    def test_post_list(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('post_list' in resp.context)
        self.assertEqual([post.pk for post in resp.context['post_list']], [2])
        self.assertFalse('post_list.has_next' in resp.context)
        self.assertFalse('post_list.has_prev' in resp.context)
